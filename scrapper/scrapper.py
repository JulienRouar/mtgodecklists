# -*- coding: utf-8 -*-

from selenium import webdriver
from collections import OrderedDict

class Scrapper():
    
    __slots__ = ('__geckodriver', '__main_url', '__decklists',
                 'driver', 
                 '__tournament_links',
                 '__names', '__scores', '__index_decklists',
                 )
    
    def __init__(self):
        self.__geckodriver = '/geckodriver-v0.26.0-win64/geckodriver.exe'
        self.__main_url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
        self.__decklists = list()
        
    def connectBrowser(self):
        self.driver = webdriver.Firefox(executable_path = self.__geckodriver)
        
    def connectURL(self, url):
        self.driver.get(url)
        
    def gatherLinks(self):
        self.__tournament_links = ['https://magic.wizards.com/en/articles/archive/mtgo-standings/pioneer-preliminary-2020-01-03']
        
    def gatherDeckLists(self):
        class_deck_meta = self.driver.find_element_by_class_name('deck-meta').text
        class_deck_meta = class_deck_meta.split('(')
        self.__names = [ self.__str_cleaner(class_deck_meta[0]) ]
        self.__scores = [ self.__str_cleaner(class_deck_meta[1]) if len(class_deck_meta)==2 else None ]
        self.__index_decklists = [0]
        
    def readDeckList(self):
        decklist = OrderedDict()
        decklist['Bloodsoaked Champion'] = 4
        return decklist
    
    def run(self):
        self.connectBrowser()
        self.connect(self.__main_url)
        self.gatherLinks()
        
        for tournament_link in self.__tournament_links:
            self.connect(tournament_link)
            self.gatherDeckLists()
            for index_decklist in self.__index_decklists:
                self.__decklists += [ self.readDeckList(index_decklist) ]
    
    def stop(self):
        self.driver.quit()
        
    def __str_cleaner(self, text):
        return text.replace(' ', '')
    
if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
    scrapper.stop()
