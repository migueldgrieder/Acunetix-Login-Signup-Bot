from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


user_data = {"Username":"user1", "Password": "pass1", "Name": "name1", "Credit card number": "1234", "E-Mail": "mail1@e.com", "Phone number": "5678", "Address": "street1"}

class ControllerBot:
    def __init__(self) -> None:
        self.setup()
        self.browser.implicitly_wait(5) 
        self.login_bot = LoginBot(self, self.browser)
        self.signup_bot = SignupBot(self)
        self.controller()

    
    def setup(self):
        
        '''#Firefox - geckodriver - Windows
        driver_path = "C:/Program Files (x86)/geckodriver.exe"
        self.browser = webdriver.Firefox(executable_path=driver_path)
        self.browser.get("http://testphp.vulnweb.com/login.php")'''

        #Chrome - chromedriver - Windows
        driver_path = "C:/Program Files (x86)/chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.browser.get("http://testphp.vulnweb.com/login.php")

    def controller(self):
        login_test = self.login_bot.do_login()
        print ("Login Test: ", login_test)
        if login_test == False:
            signup_test = self.signup_bot.do_signup()
            print ("Signup Test: ", signup_test)
            if signup_test == True:
                self.controller()
        
        
                
        
class LoginBot:
    def __init__(self, controller, browser):
        self.controller = controller
        self.browser = browser
        self.actions = ActionChains(self.browser)
    
    def do_login(self):
        self.browser.find_element_by_name("uname").send_keys("test")
        self.browser.find_element_by_name("pass").send_keys("test")
        time.sleep(1)
        login_button = self.browser.find_element_by_xpath('//*[@id="content"]/div[1]/form/table/tbody/tr[3]/td/input')
        self.actions.click(login_button)
        self.actions.perform()
        could_login = self.login_test()
        return could_login
        
    def login_test(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="globalNav"]/table/tbody/tr/td[2]/a')
            tester = True
        except:
                print( "exception - logout button not found")
                tester = False
        finally:
            return tester

class SignupBot:
    def __init__(self, controller):
        self.controller = controller
    
    def do_signup(self):
        pass

    def check_data(self):
        pass

    def go_back_login_page(self):
        pass

bot = ControllerBot()
bot()