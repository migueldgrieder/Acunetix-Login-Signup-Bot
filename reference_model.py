from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

class CookieClickerBot:
    def __init__(self) -> None:

        self.setup()
        self.browser.implicitly_wait(5) 
        self.basic_elements()
    
        self.actions = ActionChains(self.browser)
        while True:
            self.controller()
    
    def setup(self):
        
        '''#Firefox - geckodriver - Windows
        driver_path = "C:/Program Files (x86)/geckodriver.exe"
        self.browser = webdriver.Firefox(executable_path=driver_path)
        self.browser.get("https://orteil.dashnet.org/cookieclicker/")'''

        #Chrome - chromedriver - Windows
        driver_path = "C:/Users/migpl/Desktop/Code/chromedriver_win32/chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.browser.get("https://orteil.dashnet.org/cookieclicker/")

    def basic_elements(self):
        self.cookie = self.browser.find_element_by_id("bigCookie") 
        self.cookie_count = self.browser.find_element_by_id("cookies")
        self.productOwned_farm = "0" 
        self.farms = [self.browser.find_element_by_id("productPrice" + str(i)) for i in range(int(self.productOwned_farm),-1,-1)]
        

    def buy_farm(self, farm):
        actions_buy_farm = ActionChains(self.browser)
        actions_buy_farm.move_to_element(farm)
        actions_buy_farm.click(farm)
        actions_buy_farm.perform()

    
    def check_unlock_next_farm(self):
        owned_qtd_html = self.browser.find_element_by_id("productOwned" + self.productOwned_farm)
        if owned_qtd_html.text == "1":
            self.productOwned_farm = str(int(self.productOwned_farm)+1)
            self.farms = [self.browser.find_element_by_id("productPrice" + str(i)) for i in range(int(self.productOwned_farm),-1,-1)]

    def check_buy_upgrade(self, count):
        
        if count > 15:
            self.upgrade = self.browser.find_element_by_id("upgrade0")
            action_upgrade_buy = ActionChains(self.browser)
            action_upgrade_buy.move_to_element(self.upgrade)
            try:
                upgrade_price = self.browser.find_element_by_xpath('/html/body/div/div[2]/div[22]/div/div[1]/div[2]/span')
                price_upgrade_str = upgrade_price.get_attribute('innerHTML')
                price_upgrade = int(price_upgrade_str.replace(",", ''))
                if price_upgrade <= count:
                        action_upgrade_buy.click(self.upgrade)
                        action_upgrade_buy.perform()
            except:
                print( "exception on check_buy_upgrade - upgrade_price not found")
            finally:
                pass

    def check_buy_farm(self, count):
        len_farms = len(self.farms)

        for i in range(len_farms):
            price_farm_str = self.farms[i].text
            price_farm = int(price_farm_str.replace(',', ''))

            if i > 0:
                price_next_farm_str = self.farms[i-1].text
                price_next_farm = int(price_next_farm_str.replace(',', ''))

                if price_farm * 5 < price_next_farm: 
                    if price_farm <= count: 
                        self.buy_farm(self.farms[i])
            else:
                if price_farm <= count: 
                    self.buy_farm(self.farms[i])

    def controller(self):
        self.actions.click(self.cookie)
        self.actions.perform() 

        count_str = self.cookie_count.text.split(" ")[0]
        count = int(count_str.replace(',', ''))

        self.check_buy_upgrade(count)
        
        self.check_buy_farm(count)

        self.check_unlock_next_farm()
        
                

bot = CookieClickerBot()
bot()