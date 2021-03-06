# -*- coding: utf-8 -*-

import sys
from collections import OrderedDict
import pandas as pd
import numpy as np

root_path = '/'.join(sys.path[0].split('\\')[:-1])+'/'
if 'mtgodecklists' not in root_path:
    root_path += 'mtgodecklists/'
sys.path.append(root_path)
from reader import Reader, formater

class ClassifierExpertRules():
    
    __slots__ = ('__personal_path', '__formater',
                 'expert_rules',
                 )    
    
    def __init__(self, personal_path, _formater = True):
        super(ClassifierExpertRules, self).__init__()
        self.__personal_path = personal_path
        self.expert_rules = []
        if _formater:
            self.__formater = formater
        else:
            self.__formater = lambda x: x
        
    def fitExpertRules(self, filename_rules_txt):
        with open(self.__personal_path+'data/'+filename_rules_txt+'.txt', 'r') as open_file:
            decks_rules_txt = ''.join(open_file.readlines()).split('DECK')[1:]
        for deck_rule_txt in decks_rules_txt:
            tmp = deck_rule_txt.split('\n')
            deck_rules = OrderedDict({'archetype':tmp[0][1:],'expert_rules':[]})
            ind_rules = tmp.index('RULES :')
            for i in range(ind_rules+1, len(tmp)):
                if tmp[i] == 'MD :':
                    __board = 'MD'
                elif tmp[i] == 'SB :':
                    __board = 'SB'
                elif (tmp[i] != 'None') & (tmp[i] != ''):
                    deck_rules['expert_rules'] += [ExpertRule(__board, tmp[i], self.__formater)]
            self.expert_rules += [deck_rules]

    def predictExpertRules(self, decklists):
        res = pd.DataFrame([], index = range(len(decklists['MDs'])), columns = [])
        for deck_rules in self.expert_rules:
            res[deck_rules['archetype']] = [[] for i in res.index]
            for expert_rule in deck_rules['expert_rules']:
                for i, response in enumerate(expert_rule.call(decklists)):
                    res[deck_rules['archetype']].loc[i] += [response]
        return res
    
    def scoresExpertRules(self, __predictExpertRules):
        #return __predictExpertRules.applymap(lambda x:sum(x)/len(x))
        def mean_list(x):
            if type(x) == list:
                return sum(x) / len(x)
            else:
                return float(x)
        res = pd.DataFrame(0, index = __predictExpertRules.index, columns =  __predictExpertRules.columns)
        for i in res.index:
            for j in res.columns:
                res.loc[i,j] = mean_list(res.loc[i,j])
        return res
        
    def archetypesExpertRules(self, __scoresExpertRules, tol = .5):
        archetypes = __scoresExpertRules#.applymap(lambda x:__scoresExpertRules.columns[np.where((x>=tol)&(x==np.max(x)))])
        archetypes = archetypes.applymap(lambda x:'tol' if x<tol else x)
        #archetypes = archetypes.applymap(lambda x:'tie' if type(x)==list else x)
        archetypes = archetypes.apply(lambda x: archetypes.columns[np.where(x!='tol')], axis=1)
        return list(archetypes)
    
    def run(self, reader_tournaments_filenames, filenames_decklists_txt, tol = .7, 
            drop_low_freq = 0, to_csv = True):
        csv_output = pd.DataFrame(None) ; cols_output = []
        for i in range(len(reader_tournaments_filenames)):
            for j in range(len(reader_tournaments_filenames[i])):
                
                tmp = self.predictExpertRules(reader_tournaments_filenames[i][j])
                tmp2 = self.scoresExpertRules(tmp)
                reader_tournaments_filenames[i][j]['archetypes'] = [list(_)if len(list(_))!=0 else ['Other']
                                            for _ in self.archetypesExpertRules(tmp2,
                                               tol = .7)]
                cols_output += [reader_tournaments_filenames[i][j]['format'] + ' ' +
                                reader_tournaments_filenames[i][j]['type'] + ' ' +
                                reader_tournaments_filenames[i][j]['date']]
                zeta = pd.DataFrame(reader_tournaments_filenames[i][j]['archetypes'])
                
                #fix if 2 companions or 2 equal scores
                if zeta.shape[1]==2:
                    for _ in np.where(zeta.iloc[:,1].astype(str)!='None')[0]:
                        zeta.iloc[_,0] += '_'+zeta.iloc[_,1]
                    zeta = zeta.iloc[:,0]
                    #zeta = pd.concat([zeta.iloc[:,0], ],axis=0)
                    #zeta.index = range(zeta.shape[0])
                elif zeta.shape[1]>2:
                    print('PROBLEM WITH CLASSIFICATION, 3 EQUAL SCORES OR MORE !!!')
                csv_output = pd.concat([csv_output, zeta], axis = 1)
        csv_output.columns = cols_output
        
        tmp = ''
        for _ in filenames_decklists_txt:
            tmp += _
        
        csv_output[csv_output == None] = 'Other'
        if to_csv:
            csv_output.to_csv(root_path + 'data/archetypes_' + tmp + '.csv', index = None, header = True,
                          sep = ';')
        else:
            return csv_output
    
class ExpertRule():
    
    __slots__ = ('__board', '__number', '__card', '__condition', '__formater',
                 )    
    
    def __init__(self, __board, rule_txt, _formater = lambda x:x):
        super(ExpertRule, self).__init__()
        self.__formater = _formater
        self.__board = __board
        tmp = rule_txt.split(' ')
        try:
            self.__number = str(int(tmp[0])) + ' '
        except:
            self.__number = ''
        self.__card = self.__formater(' '.join(tmp[1:-1]) if self.__number != '' else ' '.join(tmp[0:-1]))
        self.__condition = tmp[-1]
        print(self.__number, self.__card, self.__condition)
        
    def call(self, decklists):
        res = []
        for i in range(len(decklists['MDs'])):
            if self.__condition == '=':
                res += [eval('"' + self.__number + self.__card + '" in decklists["'
                         + self.__board + 's"][' + str(i) + ']')]
            elif self.__condition == 'in':
                print('any(["' + self.__card + '" in _ for _ in decklists["'
                         + self.__board + 's"][' + str(i) + ']])')
                print(eval('decklists["' + self.__board + 's"][' + str(i) + ']'))
                res += [eval('any(["' + self.__card + '" in _ for _ in decklists["'
                         + self.__board + 's"][' + str(i) + ']])')]
            else:
                tmp = eval('["' + self.__card + '" in _ for _ in decklists["' +
                         self.__board + 's"][' + str(i) + ']]')
                if True in tmp:
                    res += [eval(self.__number + self.__condition +
                                 'int(decklists["' + self.__board + 's"][' + str(i) +
                        '][tmp.index(True)].split(" ")[0])')]
                else:
                    res += [False]
        return res
    
if __name__ == '__main__':
    filenames_decklists_txt = ["decklists_Standar_04_18_2020_04_30_2020"]
                                #'decklists_Modern_01_01_2020_01_05_2020',
                               #'decklists_Pioneer_01_01_2020_01_05_2020',
                               #'decklists_Modern_01_06_2020_01_11_2020',
                               #'decklists_Pioneer_01_06_2020_01_11_2020']
    filename_rules_txt = 'ExpertRulesCompanion'
    
    reader = Reader(root_path, _formater = True)
    reader_tournaments_filenames = reader.readTxtTournamentsFilenames(filenames_decklists_txt)
    #csv_output = pd.DataFrame(None)
    
    classifierExpertRules = ClassifierExpertRules('C:/Users/julie/mtgodecklists/')
    classifierExpertRules.fitExpertRules(filename_rules_txt)
    classifierExpertRules.run(reader_tournaments_filenames, filenames_decklists_txt,
                              tol = .7, to_csv = True)
    
# =============================================================================
#     cols_output = []
#     for i in range(len(res)):
#         for j in range(len(res[i])):
#             tmp = classifierExpertRules.predictExpertRules(res[i][j])
#             tmp2 = classifierExpertRules.scoresExpertRules(tmp)
#             res[i][j]['archetypes'] = [list(_)if len(list(_))!=0 else ['Other']
#                                         for _ in classifierExpertRules.archetypesExpertRules(tmp2,
#                                            tol = .7)]
#             cols_output += [res[i][j]['format'] + ' ' + res[i][j]['type'] + ' ' + res[i][j]['date']]
#             csv_output = pd.concat([csv_output, pd.DataFrame(res[i][j]['archetypes'])], axis = 1)
#     csv_output.columns = cols_output
#     
#     tmp = ''
#     for _ in filenames_decklists_txt:
#         tmp += _
#     
#     csv_output[csv_output == None] = 'Other'
#     csv_output.to_csv(root_path + 'data/archetypes_' + tmp + '.csv', index = None, header = True,
#                       sep = ';')
# =============================================================================
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#FOR MACHINE LEARNING
# =============================================================================
#     def buildsPandasDataFrame(self, decklists):
#         pass
#     
#     def fitLightGBM(self, df_decklists):
#         pass
#     
#     def predictLightGBM(self, df_decklists):
#         pass
# =============================================================================
    