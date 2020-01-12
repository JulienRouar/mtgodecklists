# -*- coding: utf-8 -*-

from reader import Reader
from collections import OrderedDict
import pandas as pd
import numpy as np

class ClassifierExpertRules():
    
    __slots__ = ('__personal_path',
                 'expert_rules',
                 )    
    
    def __init__(self, personal_path):
        super(ClassifierExpertRules, self).__init__()
        self.__personal_path = personal_path
        self.expert_rules = []
        
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
                    deck_rules['expert_rules'] += [ExpertRule(__board, tmp[i])]
            self.expert_rules += [deck_rules]

    def predictExpertRules(self, decklists):
        res = pd.DataFrame([], index = range(len(decklists['MDs'])), columns = [])
        for deck_rules in self.expert_rules:
            res[deck_rules['archetype']] = [[] for i in res.index]
            print('archetype :', deck_rules['archetype'], len(deck_rules['expert_rules']))
            for expert_rule in deck_rules['expert_rules']:
                for i, response in enumerate(expert_rule.call(decklists)):
                    res[deck_rules['archetype']].loc[i] += [response]
        return res
    
    def scoresExpertRules(self, __predictExpertRules):
        return __predictExpertRules.applymap(lambda x:sum(x)/len(x))
    
    def archetypesExpertRules(self, __scoresExpertRules, tol = .9):
        archetypes = __scoresExpertRules.applymap(lambda x:__scoresExpertRules.columns[np.where((x>tol)&(x==np.max(x)))])
        archetypes = archetypes.applymap(lambda x:'tol' if len(x)==0 else x[0])
        archetypes = archetypes.applymap(lambda x:'tie' if type(x)==list else x)
        return archetypes
    
class ExpertRule():
    
    __slots__ = ('__board', '__number', '__card', '__condition',
                 )    
    
    def __init__(self, __board, rule_txt):
        super(ExpertRule, self).__init__()
        self.__board = __board
        tmp = rule_txt.split(' ')
        try:
            self.__number = str(int(tmp[0])) + ' '
        except:
            self.__number = ''
        self.__card = ' '.join(tmp[1:-1]) if self.__number != '' else ' '.join(tmp[0:-1])
        self.__condition = tmp[-1]
        
    def call(self, decklists):
        res = []
        for i in range(len(decklists['MDs'])):
            if self.__condition == '=':
                res += [eval('"' + self.__number + self.__card + '" in decklists["'
                         + self.__board + 's"][' + str(i) + ']')]
            elif self.__condition == 'in':
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
    filenames_decklists_txt = [#'decklists_Modern_01_01_2020_01_05_2020',
                               'decklists_Pioneer_01_01_2020_01_05_2020',
                               #'decklists_Modern_01_06_2020_01_11_2020',
                               'decklists_Pioneer_01_06_2020_01_11_2020']
    filename_rules_txt = 'ExpertRulesPioneer'
    
    reader = Reader('C:/Users/julie/mtgodecklists/')
    res = reader.readTxtTournamentsFilenames(filenames_decklists_txt)
    
    classifierExpertRules = ClassifierExpertRules('C:/Users/julie/mtgodecklists/')
    classifierExpertRules.fitExpertRules(filename_rules_txt)
    
    for i in range(len(res)):
        for j in range(len(res[i])):
            tmp = classifierExpertRules.predictExpertRules(res[i][j])
            tmp2 = classifierExpertRules.scoresExpertRules(tmp)
            res[i][j]['archetypes'] = classifierExpertRules.archetypesExpertRules(tmp2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    