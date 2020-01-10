# -*- coding: utf-8 -*-

class Classifier():
    
    __slots__ = ('__personal_path',
                 )    
    
    def __init__(self, personal_path):
        super(Classifier, self).__init__()
        self.__personal_path = personal_path
        
    def fitExpertRules(self, config_txt):
        pass
    
    def predictExpertRules(self, decklists):
        pass
    
    def buildsPandasDataFrame(self, decklists):
        pass
    
    def fitLightGBM(self, df_decklists):
        pass
    
    def predictLightGBM(self, df_decklists):
        pass
    