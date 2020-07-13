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
        
    def __number_transformer(self, _float):
        return round(_float*100, 4)
        
    def distributionSummary(self, decklists_name, archetypes_name, archetypes_expected=None,
                            drop_other = False, drop_leagues = False, drop_low_freq = 0, total_companions = False):
        with open(self.__personal_path+'data/'+decklists_name+'.txt', 'r') as open_file:
            decklists = open_file.readlines()
        archetypes = pd.read_csv(self.__personal_path+'data/'+archetypes_name+'.csv', delimiter=';')

        unique_archetypes = np.concatenate([archetypes[c].unique() for c in archetypes.columns])
        unique_archetypes = set(list(unique_archetypes[np.where(unique_archetypes==unique_archetypes)[0]]))
        data = pd.DataFrame(0, index = archetypes.columns, columns = unique_archetypes)
        
        for c in archetypes.columns:
            temp = archetypes[c].value_counts()
            for d in temp.index:
                if d in temp.index:
                    data[d][c] = temp[d]
        if archetypes_expected:
            for c in archetypes_expected:
                if c not in data.columns:
                    data[c] = 0
            print(data.columns)
            data = pd.concat([data[archetypes_expected], data['Other']], axis = 1)
            print(data.columns)
        
        if drop_leagues:
            for i in data.index:
                if 'League' in i:
                    data.drop(i, inplace = True, axis = 0)
        if float(drop_low_freq)>0:
            tot = data.sum().sum()
            for c in data.columns[:-1]:
                if (data[c].sum()/tot)<drop_low_freq:
                    data['Other'] += data[c]
                    data.drop(c, inplace = True, axis = 1)
        if drop_other:
            data.drop('Other', inplace = True, axis = 1)
        
        cols = data.columns
        data = data.astype(int)
        
        if total_companions:
            cards_decklists = (archetypes.isna() == False).sum(axis = 0)
            cards_companions = ((archetypes != 'Other')&(archetypes.isna() == False)).sum(axis = 0)
            
            data['%listes avec compagnon'] = [self.__number_transformer(_)
                                                    for _ in cards_companions/cards_decklists]
           
            data = pd.concat([pd.DataFrame(None, index = ['Total'], columns = data.columns), data])
            
            if archetypes_expected:
                for c in data.columns[:-1]:
                    if c not in archetypes_expected:
                        c1 = c.split('_')[0] ; c2 = c.split('_')[1]
                        data[c1] += data[c] ; data[c2] += data[c]
                        data.drop(c, inplace = True, axis = 1)
                cols = data.columns[:-1]
            data['%listes avec compagnon'].loc['Total'] = self.__number_transformer(cards_companions.sum()/cards_decklists.sum())                                                    
            #data[cols].loc['Total'] = [self.__number_transformer(_) for _ in data[cols].sum(axis = 0) / cards_decklists.sum() ]
            for i, _ in enumerate([self.__number_transformer(_) for _ in data[cols].sum(axis = 0) / cards_decklists.sum()]):
                data[cols[i]].loc['Total'] = _
        else:
            cards_decklists = (archetypes.isna() == False).sum(axis = 0)
            cards_companions = ((archetypes != 'Other')&(archetypes.isna() == False)).sum(axis = 0)
            
            data['%listes avec compagnon'] = [self.__number_transformer(_)
                                                    for _ in cards_companions/cards_decklists]
           
            data = pd.concat([pd.DataFrame(None, index = ['Total'], columns = data.columns), data])
            
            if archetypes_expected:
                for c in data.columns[:-1]:
                    if c not in archetypes_expected:
                        c1 = c.split('_')[0] ; c2 = c.split('_')[1]
                        data[c1] += data[c] ; data[c2] += data[c]
                        data.drop(c, inplace = True, axis = 1)
                cols = data.columns[:-1]
            data['%listes avec compagnon'].loc['Total'] = self.__number_transformer(cards_companions.sum()/cards_decklists.sum())                                                    
            #data[cols].loc['Total'] = [self.__number_transformer(_) for _ in data[cols].sum(axis = 0) / cards_decklists.sum() ]
            for i, _ in enumerate([self.__number_transformer(_) for _ in data[cols].sum(axis = 0) / cards_decklists.sum()]):
                data[cols[i]].loc['Total'] = _

        data['Links'] = decklists[1:(data.shape[0]+1)] ; data['Links'] = data['Links'].shift(1)
        data = pd.concat([pd.DataFrame(list(cards_decklists) + [''],
                                index = data.index, columns = ['# Decklists']), data], axis = 1)
        data['# Decklists'] = data['# Decklists'].shift(1)
        data['# Decklists'].iloc[0] = data['# Decklists'].iloc[1:].sum()
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