# -*- coding: utf-8 -*-

from .reader import Reader

class Classifier():
    
    __slots__ = ('__personal_path',
                 )    
    
    def __init__(self, personal_path):
        super(Classifier, self).__init__()
        self.__personal_path = personal_path
        
    def fitExpertRules(self, rules_txt):
        pass
    
    def predictExpertRules(self, decklists):
        pass
    
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
    