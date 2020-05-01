# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np

root_path = '/'.join(sys.path[0].split('\\')[:-1])+'/'
if 'mtgodecklists' not in root_path:
    root_path += 'mtgodecklists/'
sys.path.append(root_path)

class Stater():
    
    __slots__ = ('__personal_path',
                 )    
    
    def __init__(self, personal_path):
        super(Stater, self).__init__()
        self.__personal_path = personal_path
        
    def distributionSummary(self, decklists_name, archetypes_name, archetypes_expected=None,
                            drop_other = False, drop_leagues = False):
        with open(self.__personal_path+'data/'+decklists_name+'.txt', 'r') as open_file:
            decklists = open_file.readlines()
        archetypes = pd.read_csv(self.__personal_path+'data/'+archetypes_name+'.csv', delimiter=';')
        if not archetypes_expected:
            unique_archetypes = np.concatenate([archetypes[c].unique() for c in archetypes.columns])
            unique_archetypes = set(list(unique_archetypes[np.where(unique_archetypes==unique_archetypes)[0]]))
            data = pd.DataFrame(0, index = archetypes.columns, columns = unique_archetypes)
        else:
            data = pd.DataFrame(0, index = archetypes.columns, columns = archetypes_expected+['Other'])
        
        for c in archetypes.columns:
            temp = archetypes[c].value_counts()
            for d in temp.index:
                if d in temp.index:
                    data[d][c] = temp[d]
        
        data['Links'] = decklists[1:(data.shape[0]+1)]
        if drop_other:
            data.drop('Other', inplace = True, axis = 1)
        if drop_leagues:
            for i in data.index:
                if 'League' in i:
                    data.drop(i, inplace = True, axis = 0)
        data = data.loc[[_ for _ in reversed(data.index)]]
        data.to_csv(self.__personal_path+'data/distributionSummary_'+
                    '_'.join(decklists_name.split('_')[1:])+'.csv', sep=';')
        
if __name__ == '__main__':
    decklists_name = 'decklists_Standar_04_18_2020_04_30_2020'
    archetypes_name = 'archetypes_decklists_Standar_04_18_2020_04_30_2020'
    companions = ['Gyruda, Doom of Depths','Jegantha, the Wellspring','Kaheera, the Orphanguard',
                  'Keruga, the Macrosage','Lurrus of the Dream-Den','Lutri, the Spellchaser',
                  'Obosh, the Preypiercer','Umori, the Collector',
                  'Yorion, Sky Nomad','Zirda, the Dawnwaker']
    Stater(root_path).distributionSummary(decklists_name, archetypes_name, archetypes_expected=companions,
                            drop_other = True, drop_leagues = True)
    
    #anael.yahi@gmail.com