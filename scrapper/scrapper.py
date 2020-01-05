# -*- coding: utf-8 -*-

from selenium import webdriver
from collections import OrderedDict

class Scrapper():
    
    __slots__ = ('__personal_path', '__geckodriver', '__main_url', '__decklists',
                 'driver', 
                 '__tournament_links',
                 '__names', '__scores', '__index_decklists',
                 )
    
    def __init__(self, personal_path):
        super(Scrapper, self).__init__()
        self.__personal_path = personal_path
        self.__geckodriver = self.__personal_path + 'geckodriver-v0.26.0-win64/geckodriver.exe'
        self.__main_url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
        self.__decklists = list()
        
    def connectBrowser(self):
        self.driver = webdriver.Firefox(executable_path = self.__geckodriver)
        
    def connectURL(self, url):
        self.driver.get(url)
        
    def gatherLinks(self):
        self.__tournament_links = ['https://magic.wizards.com/en/articles/archive/mtgo-standings/pioneer-preliminary-2020-01-03']
        
    def gatherDeckLists(self):
        class_deck_meta = [ element.text.split('\n')[0] for element in self.driver.find_elements_by_class_name('deck-meta') ]
        self.__names = [ ' '.join(element_text.split(' ')[:-1]) for element_text in class_deck_meta ]
        self.__scores = [ ( element_text.split(' ')[-1] if len(element_text.split(' '))>1 else None ) for element_text in class_deck_meta]
        self.__index_decklists = [ i for i in self.__names ]
        
    def readDeckList(self, index_decklist):
        decklist = OrderedDict()
        decklist['Bloodsoaked Champion'] = 4
        return decklist
    
    def run(self):
        self.connectBrowser()
        self.connectURL(self.__main_url)
        self.gatherLinks()
        
        for tournament_link in self.__tournament_links:
            self.connectURL(tournament_link)
            self.gatherDeckLists()
            for index_decklist in self.__index_decklists:
                self.__decklists += [ self.readDeckList(index_decklist) ]
                
    def to_txt(self, filename):
        pass
    
    def stop(self):
        self.driver.quit()
        
    def __str_cleaner(self, text):
        pass
    
if __name__ == '__main__':
    scrapper = Scrapper(personal_path = 'C:/Users/julie/mtgodecklists/')
    scrapper.run()
    scrapper.stop()
    scrapper.to_txt(filename = 'results.txt')

#test / in progress stuff
if False:
    driver = webdriver.Firefox(executable_path = 'C:/Users/julie/mtgodecklists/geckodriver-v0.26.0-win64/geckodriver.exe')
    driver.get('https://magic.wizards.com/en/articles/archive/mtgo-standings/pioneer-preliminary-2020-01-03')
    class_deck_meta = [ res.text for res in driver.find_elements_by_class_name('deck-meta')]
    #class_deck_meta = class_deck_meta.split('(')
    print(class_deck_meta)
    
    driver.quit()



    
    
    
    
    
    
    
    
    
    