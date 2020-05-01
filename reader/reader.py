# -*- coding: utf-8 -*-

from collections import OrderedDict
import sys

def formater(card_name):
    res = card_name.lower()
    for sign in [',', '/', '//', '-', '  ']:
        res = ' '.join(res.split(sign))
    return res

class Reader():
    
    __slots__ = ('__personal_path',
                 'decklists', '__card_types',  '__formater',
                 )    
    
    def __init__(self, personal_path, _formater = True):
        super(Reader, self).__init__()
        self.__personal_path = personal_path
        self.decklists = []
        self.__card_types = ['Creature', 'Sorcery', 'Instant', 'Artifact', 'Enchantement',
                             'Planeswalker', 'Tribal', 'Land']
        if _formater:
            self.__formater = formater
        else:
            self.__formater = lambda x: x

    def readTxtTournamentsFilename(self, filename_tournaments_txt):
        __tournaments = []
        
        with open(self.__personal_path+'data/'+filename_tournaments_txt+'.txt', 'r') as open_file:
            lines = ''.join(open_file.readlines())
        
        lines = lines.split('CATEGORY')
        del lines[0]
        
        while len(lines) > 0:
            __tournament = OrderedDict({'format':None, 'type':None, 'date':None,
                                    'metas':[], 'MDs':[], 'SBs':[], 'archetypes':[]})
            lines_tournament = lines[0]
            lines_tournament = lines_tournament.split('DECKLIST')
            
            tmp = lines_tournament[0].split('\n')
            __tournament['format'] = tmp[1].split(' ')[0]
            __tournament['type'] = tmp[1].split(' ')[1]
            __tournament['date'] = ' '.join(tmp[2:])
            del lines_tournament[0]
            
            while len(lines_tournament) > 0:
                tmp = lines_tournament[0].split('\n')
                __tournament['metas'] += [tmp[1] + ';' + tmp[2]]
                tmp = tmp[1:-1]
                lim_sb = ['Sideboard' in _ for _ in tmp].index(True)
                __tournament['MDs'] += [[self.__formater(_) for _ in tmp[2:lim_sb]]]
                __tournament['SBs'] += [[self.__formater(_) for _ in tmp[(lim_sb+1):]]]
                for ind_sb in range(len(__tournament['SBs'])):
                    while '' in __tournament['SBs'][ind_sb]:
                        del __tournament['SBs'][ind_sb][__tournament['SBs'][ind_sb].index('')]
                del lines_tournament[0]
            
            __tournaments += [__tournament]
            del lines[0]
            
        return __tournaments
                        
    def readTxtTournamentsFilenames(self, filenames_tournaments_txt):
        __tournaments = []
        for filename_tournaments_txt in filenames_tournaments_txt:
            __tournaments += [self.readTxtTournamentsFilename(filename_tournaments_txt)]
        return __tournaments
        
if __name__ == '__main__':
    filenames_decklists_txt = ['decklists_Modern_01_01_2020_01_05_2020',
                               'decklists_Pioneer_01_01_2020_01_05_2020',
                               'decklists_Modern_01_06_2020_01_11_2020',
                               'decklists_Pioneer_01_06_2020_01_11_2020']
    root_path = '/'.join(sys.path[0].split('\\')[:-1])+'/'
    if 'mtgodecklists' not in root_path:
        root_path += 'mtgodecklists/'
    reader = Reader(root_path, _formater = True)
    res = reader.readTxtTournamentsFilenames(filenames_decklists_txt)