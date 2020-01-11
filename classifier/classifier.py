# -*- coding: utf-8 -*-

from .reader import Reader
from collections import OrderedDict
import pandas as pd
import numpy as np

class Classifier():
    
    __slots__ = ('__personal_path',
                 'expert_rules',
                 )    
    
    def __init__(self, personal_path):
        super(Classifier, self).__init__()
        self.__personal_path = personal_path
        self.expert_rules = []
        
    def fitExpertRules(self, filename_rules_txt):
        with open(self.__personal_path+'data/'+filename_rules_txt+'.txt', 'r') as open_file:
            decks_rules_txt = open_file.readlines().split('DECK')
        for deck_rule_txt in decks_rules_txt:
            tmp = deck_rule_txt.split('\n')
            deck_rules = OrderedDict({'archetype':tmp[0][1:],'expert_rules':[]})
            ind_rules = tmp.index('RULES :')
            for i in range(ind_rules+1, len(tmp)):
                if tmp[i] == 'MD :':
                    __board = 'MD'
                elif tmp[i] == 'SB :':
                    __board = 'SB'
                else:
                    deck_rules['expert_rules'] += [ExpertRule(__board, tmp[i])]
            self.expert_rules += [deck_rules]

    def predictExpertRules(self, decklists):
        res = pd.DataFrame([], index = range(len(decklists)), columns = [])
        for deck_rules in self.expert_rules:
            res[deck_rules['archetype']] = []
            for expert_rule in deck_rules['expert_rules']:
                for i, decklist in enumerate(decklists):
                    res[deck_rules['archetype']].loc[i] += expert_rule.call(decklist)
        return res
    
    def scoresExpertRules(self, __predictExpertRules):
        return __predictExpertRules.apply(lambda x:sum(x)/len(x))
    
    def archetypesExpertRules(self, __scoresExpertRules, tol = .9):
        archetypes = __scoresExpertRules.apply(lambda x:__scoresExpertRules.index[np.where((x>tol)&(x==np.max(x)))])
        archetypes = archetypes.apply(lambda x:'tol' if len(x.shape)==0 else x)
        archetypes = archetypes.apply(lambda x:'tie' if x.shape[0]>1 else x)
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
        self.__condition = tmp[-1] if tmp[-1] != '=' else '=='
        
    def call(self, decklists):
        return [eval(self.__number + self.__card + ' ' + self.__condition + ' decklists['
                     + self.__board + 's][' + str(i) + ']') for i in range(len(decklists['MDs']))]
    
if __name__ == '__main__':
    filenames_decklists_txt = ['decklists_Modern_01_01_2020_01_05_2020',
                               'decklists_Pioneer_01_01_2020_01_05_2020',
                               'decklists_Modern_01_06_2020_01_11_2020',
                               'decklists_Pioneer_01_06_2020_01_11_2020']
    
    reader = Reader('C:/Users/julie/mtgodecklists/')
    res = reader.readTxtTournamentsFilenames(filenames_decklists_txt)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    