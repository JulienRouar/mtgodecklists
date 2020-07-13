# -*- coding: utf-8 -*-

from collections import OrderedDict
import pandas as pd
import sys

root_path = '/'.join(sys.path[0].split('\\')[:-1])+'/'
if 'mtgodecklists' not in root_path:
    root_path += 'mtgodecklists/'
sys.path.append(root_path)

from scrapper import Scrapper
from reader import Reader
from classifier import ClassifierExpertRules
from stater import Stater

with open(root_path+'config.txt', 'r') as open_file:
   file_config = open_file.readlines()

config = OrderedDict()
for line in file_config:
    if '=' in line:
        config[line.split('=')[0]] = line.split('=')[1].split('\n')[0]
for c in config:
    if config[c] == 'True':
        config[c] = True
    elif config[c] == 'False':
        config[c] = False
    
    
    
#FILES
filenames_decklists_txt = ["decklists_"+config['FORMAT']+config['TYPE']+"_"+config['DATE_FROM'].split('/')[0]+
                           "_"+config['DATE_FROM'].split('/')[1]+"_"+config['DATE_FROM'].split('/')[2]+
                           "_"+config['DATE_TO'].split('/')[0]+"_"+config['DATE_TO'].split('/')[1]+
                           "_"+config['DATE_TO'].split('/')[2]]

if (config['RULES'] in['Companion', 'Modern']):
    filename_rules_txt = 'ExpertRules' + config['RULES']
    #if (config['EXPECTED_TARGETS'] == 'Companion') or (config['EXPECTED_TARGETS'] == 'Metagame'):
    with open(root_path+'data/'+filename_rules_txt+'.txt', 'r') as open_file:
        rules = open_file.readlines()
    archetypes_expected = []
    for line in rules:
        if 'DECK ' in line:
            archetypes_expected += [line.split('DECK ')[1].split('\n')[0]]
    #elif config['EXPECTED_TARGETS'] == 'False':
        #archetypes_expected = False
    
    
   
# =============================================================================
# #SCRAPPING
# scrapper = Scrapper(root_path,
#              {'from_date' : config['DATE_FROM'], 'to_date' : config['DATE_TO'],
#               'format': config['FORMAT'], 'type': config['TYPE']}, drop_leagues = config['DROP_LEAGUES'])
# scrapper.run()
# scrapper.stop()
# scrapper.writeFileText(scrapper.decklists, scrapper.metas)
# =============================================================================



#CLASSIFIYING
reader = Reader(root_path, _formater = config['STRING_CLEANER'])
reader_tournaments_filenames = reader.readTxtTournamentsFilenames(filenames_decklists_txt)

classifierExpertRules = ClassifierExpertRules(root_path, _formater = 'True'==config['STRING_CLEANER'])
classifierExpertRules.fitExpertRules(filename_rules_txt)
classifierExpertRules.run(reader_tournaments_filenames, filenames_decklists_txt,
                          tol = float(config['RULES_TOLERANCE']), to_csv = True)
    


# =============================================================================
# #STATS
# decklists_name = 'decklists_' + '_'.join(filenames_decklists_txt[0].split('_')[1:])
# archetypes_name = 'archetypes_decklists_' + '_'.join(filenames_decklists_txt[0].split('_')[1:])
# 
# Stater(root_path).distributionSummary(decklists_name, archetypes_name,
#       archetypes_expected=archetypes_expected, drop_other = config['DROP_OTHER'],
#       drop_leagues = config['DROP_LEAGUES'], drop_low_freq = config['DROP_LOW_FREQ'],
#       total_companions = config['RULES'] == 'Companion')
# =============================================================================


