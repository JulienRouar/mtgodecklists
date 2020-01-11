# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 16:57:35 2020

@author: julie
"""

from collections import OrderedDict

class Reader():
    
    __slots__ = ('__personal_path',
                 'decklists', '__card_types', 
                 )    
    
    def __init__(self, personal_path):
        super(Reader, self).__init__()
        self.__personal_path = personal_path
        self.decklists = []
        self.__card_types = ['Creature', 'Sorcery', 'Instant', 'Artifact', 'Enchantement',
                             'Planeswalker', 'Tribal', 'Land']

    def readTxtTournamentsFilename(self, filename_tournaments_txt):
        __tournaments = []
        __tournament = OrderedDict({'format':None, 'type':None, 'date':None,
                                    'metas':[], 'decklists':[], 'archetypes':[]})
        
        with open(self.__personal_path+'data/'+filename_tournaments_txt+'.txt', 'r') as open_file:
            lines = open_file.readlines()
            
        lines = lines.split('CATEGORY')
        del lines[0]
        
        while len(lines) > 0:
            lines_tournament = lines[0]
            lines_tournament = lines_tournament.split('DECKLIST')
            
            tmp = lines_tournament[0].split('\n')
            __tournament['format'] = tmp[0].split(' ')[0]
            __tournament['type'] = tmp[0].split(' ')[1]
            __tournament['date'] = ' '.join(tmp[1:])
            del lines_tournament[0]
            
            while len(lines_tournament) > 0:
                tmp = lines_tournament[0].split('\n')
                __tournament['metas'] += [(' '.join(tmp[0].split(' ')[:-1]), tmp[0].split(' ')[-1])]
                __tournament['decklists'] += [tmp[1:-1]]
                del lines_tournament[0]
            
            __tournaments += __tournament
            del lines[0]
            
            return __tournaments
                        
        def readTxtTournamentsFilenames(self, filenames_tournaments_txt):
            __tournaments = []
            for filename_decklists_txt in filenames_tournaments_txt:
                __tournaments += self.readTxtTournamentsFilename(filename_tournaments_txt)
            return __tournaments
        
if __name__ == '__main__':
    filenames_decklists_txt = ['decklists_Modern_01_01_2020_01_05_2020',
                               'decklists_Pioneer_01_01_2020_01_05_2020',
                               'decklists_Modern_01_06_2020_01_11_2020',
                               'decklists_Pioneer_01_06_2020_01_11_2020']
    
    reader = Reader('C:/Users/julie/mtgodecklists/')
    res = reader.readTxtTournamentsFilenames(filenames_decklists_txt)