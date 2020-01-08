# -*- coding: utf-8 -*-

from selenium import webdriver
from collections import OrderedDict
from time import sleep

class Scrapper():
    
    __slots__ = ('__personal_path', '__geckodriver', '__main_url', 'decklists', '__card_types', 'params', 
                 'driver', 
                 '__titles', '__dates', '__tournament_links',
                 '__names', '__scores', '__raw_decklists',
                 'decklists',
                 )    
    
    def __init__(self, personal_path, params = None):
        super(Scrapper, self).__init__()
        self.__personal_path = personal_path
        self.__geckodriver = self.__personal_path + 'geckodriver-v0.26.0-win64/geckodriver.exe'
        self.__main_url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
        self.decklists = list()
        self.__card_types = ['Creature', 'Sorcery', 'Instant', 'Artifact', 'Enchantement',
                             'Planeswalker', 'Tribal', 'Land']
        self.params = params
        if self.params is None:
            self.params = OrderedDict({'from_date' : '01/04/2020', 
                                       'to_date' : '01/07/2020',
                                       'research': 'Pioneer'})
        
    def connectBrowser(self):
        self.driver = webdriver.Firefox(executable_path = self.__geckodriver)
        
    def connectURL(self, url):
        self.driver.get(url)
        try:
            sleep(2)
            class_button_agree = self.driver.find_element_by_class_name('button.agree')
            class_button_agree.click()
            sleep(2)
        except:
            pass
        
    def filterLinks(self):
        id_datepickerFrom = self.driver.find_element_by_id('datepickerFrom')
        id_datepickerFrom.send_keys(self.params['from_date'])
        id_datepickerTo = self.driver.find_element_by_id('datepickerTo')
        id_datepickerTo.send_keys(self.params['to_date'])
        class_form_text = self.driver.find_element_by_class_name('form-text')
        class_form_text.send_keys(self.params['research'])
        class_custom_search_submit = self.driver.find_element_by_class_name('item-wrap.search-btn.see-more-article-listing-section-search')
        class_custom_search_submit = class_custom_search_submit.find_element_by_id('custom-search-submit')
        self.driver.execute_script("arguments[0].click();", class_custom_search_submit)
        sleep(2)
        
    def scrollerLinks(self):
        class_see_more_archives = self.driver.find_element_by_class_name('see-more.see-more-article-listing-section')
        __next = True
        while __next:
            try:
                class_see_more_archives.click()
                class_see_more_archives = self.driver.find_element_by_class_name('see-more.see-more-article-listing-section')
                sleep(2)
            except:
                __next = False
        
    def gatherLinks(self):
        self.__titles = [ element.text for element in self.driver.find_elements_by_class_name('title') ]
        self.__dates = [ element.text for element in self.driver.find_elements_by_class_name('date') ]
        elems = self.driver.find_elements_by_css_selector('div.article-item-extended >a')
        self.__tournament_links = [ element.get_attribute("href") for element in elems ]
    
    def gatherDeckLists(self):
        class_deck_meta = [ element.text.split('\n')[0] for element in self.driver.find_elements_by_class_name('deck-meta') ]
        self.__names = [ ' '.join(element_text.split(' ')[:-1]) for element_text in class_deck_meta ]
        self.__scores = [ ( element_text.split(' ')[-1] if len(element_text.split(' '))>1 else None ) for element_text in class_deck_meta]
        self.__raw_decklists = [ element.text for element in self.driver.find_elements_by_class_name('deck-list-text') ]
        
    def readDeckList(self, __raw_decklists):
        return [ self.textDeckList(decklist) for decklist in __raw_decklists ]
        #return [ self.parserDeckList(decklist) for decklist in __raw_decklists ]
    
    def parserDeckList(self, str_decklist):
        dict_decklist = OrderedDict()
        dict_decklist['Types'] = OrderedDict(dict([(card_type, 0) for card_type in self.__card_types]))
        dict_decklist['MD'] = OrderedDict()
        dict_decklist['SB'] = OrderedDict()
        
        str_decklist = str_decklist.split('Sideboard')
        str_md = str_decklist[0].split('\n')
        str_sb = str_decklist[1].split('\n')
        
        dict_decklist['SB']['Count'] = str_sb[0].split('(')[-1].split(')')[0]
        try:
            dict_decklist['SB']['Count'] = int(dict_decklist['SB']['Count'])
            dict_decklist['SB']['SB'] = str_sb[1]
        except:
            dict_decklist['SB']['Count'] = None
        
        __next = True
        for row in str_md:
            if __next:
                row_split = (' '.join(row.split(' ')[1:]), row.split(' ')[0])
                if any([card_type in row for card_type in self.__card_types]):
                    try:
                        dict_decklist['Types'][row_split[1]] = row_split[0].split('(')[-1].split(')')[0]
                    except:
                        dict_decklist['Types'][row_split[1]] = None
                elif 'Cards' not in row:
                    try:
                        dict_decklist['MD'][row_split[0]] = int(row_split[1])
                    except:
                        dict_decklist['MD'][row_split[1]] = None
                else:
                    __next = False
            else:
                pass        
        
        return dict_decklist
    
    def textDeckList(self, str_decklist):
        return str_decklist.split('\n')
        
    def writeFileText(self, decklists):
        pass
    
    def writeFileCsv(self, decklists):
        pass
    
    def run(self):
        self.connectBrowser()
        self.connectURL(self.__main_url)
        self.filterLinks()
        self.scrollerLinks()
        self.gatherLinks()
        
        for tournament_link in self.__tournament_links:
            self.connectURL(tournament_link)
            self.gatherDeckLists()
            self.decklists = self.readDeckList(self.__raw_decklists)
            print(self.decklists[:2])
            sleep(2)
        self.stop()
    
    def stop(self):
        self.driver.quit()
        
    def __str_cleaner(self, text):
        pass
    
if __name__ == '__main__':
    scrapper = Scrapper(personal_path = 'C:/Users/julie/mtgodecklists/')
    scrapper.run()#{'from_date':,'to_date':,'research':})
    scrapper.stop()
    scrapper.writeFileText(scrapper.decklists)

#test / in progress stuff
if False:
    driver = webdriver.Firefox(executable_path = 'C:/Users/julie/mtgodecklists/geckodriver-v0.26.0-win64/geckodriver.exe')
    driver.get('https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info')
    
    
    id_date_picker_from = driver.find_element_by_id('datepickerFrom')
    id_date_picker_from.send_keys('01/01/2020')
    id_date_picker_to = driver.find_element_by_id('datepickerTo')
    id_date_picker_to.send_keys('01/06/2020')
    driver.find_element_by_class_name('form-text').send_keys('Pioneer')
    class_custom_search_submit = driver.find_element_by_class_name('item-wrap.search-btn.see-more-article-listing-section-search')
    class_custom_search_submit = class_custom_search_submit.find_element_by_id('custom-search-submit')
    driver.execute_script("arguments[0].click();", class_custom_search_submit)
    sleep(3)
    
    
    class_see_more_archives = driver.find_element_by_class_name('see-more.see-more-article-listing-section')
    __next = True
    while __next:
        try:
            class_see_more_archives.click()
            #maybe wait something ?
            class_see_more_archives = driver.find_element_by_class_name('see-more.see-more-article-listing-section')
            sleep(2)
        except:
            __next = False
            
            
    titles = [ element.text for element in driver.find_elements_by_class_name('title') ]
    dates = [ element.text for element in driver.find_elements_by_class_name('date') ]
    elems = driver.find_elements_by_css_selector('div.article-item-extended >a')
    class_article_item_extended = [ element.get_attribute("href") for element in elems ]

    
    sublinks = [ element for element in class_article_item_extended ]
    __raw_decklists = [ None for sublink in sublinks ] ; i = -1
    for sublink in sublinks:
        driver.get(sublink)
        ### read decklist
        sleep(1) ; i += 1
        __raw_decklists[i] = [ element.text for element in driver.find_elements_by_class_name('deck-list-text') ]
        sleep(3)
        
        
    driver.quit()
    
    __card_types = ['Creature', 'Sorcery', 'Instant', 'Artifact', 'Enchantement',
                             'Planeswalker', 'Tribal', 'Land']
    def parserDeckList(str_decklist):
        dict_decklist = OrderedDict()
        dict_decklist['Types'] = OrderedDict(dict([(card_type, 0) for card_type in __card_types]))
        dict_decklist['MD'] = OrderedDict()
        dict_decklist['SB'] = OrderedDict()
        
        str_decklist = str_decklist.split('Sideboard')
        str_md = str_decklist[0].split('\n')
        str_sb = str_decklist[1].split('\n')
        
        dict_decklist['SB']['Count'] = str_sb[0].split('(')[-1].split(')')[0]
        try:
            dict_decklist['SB']['Count'] = int(dict_decklist['SB']['Count'])
            dict_decklist['SB']['SB'] = str_sb[1]
        except:
            dict_decklist['SB']['Count'] = None
        
        __next = True
        for row in str_md:
            if __next:
                row_split = (' '.join(row.split(' ')[1:]), row.split(' ')[0])
                if any([card_type in row for card_type in __card_types]):
                    try:
                        dict_decklist['Types'][row_split[1]] = row_split[0].split('(')[-1].split(')')[0]
                    except:
                        dict_decklist['Types'][row_split[1]] = None
                elif 'Cards' not in row:
                    try:
                        dict_decklist['MD'][row_split[0]] = int(row_split[1])
                    except:
                        dict_decklist['MD'][row_split[1]] = None
                else:
                    __next = False
            else:
                pass        
        
        return dict_decklist
    
    
    
    
    
    
    
    
    
    
    
    