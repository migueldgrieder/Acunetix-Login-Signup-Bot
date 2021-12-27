from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



user_data = {"Username":"user1", "Password": "pass1", "Name": "name1", "Credit card": "1234", "E-Mail": "mail1@e.com", "Phone number": "5678", "Address": "street1"}

class ControllerBot:
    def __init__(self) -> None:
        self.setup()
        self.browser.implicitly_wait(5) 
        self.login_bot = LoginBot(self, self.browser)
        self.signup_bot = SignupBot(self, self.browser)
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
        test_list = []
        login_test = self.login_bot.do_login()
        test_list.append(login_test)
        if login_test == False:
            (signup_test, error_counter) = self.signup_bot.do_signup()
            test_list.append(signup_test)
            test_list.append(error_counter)
            if signup_test == True:
                second_login_test = self.login_bot.do_login()
                test_list.append(second_login_test)
        self.print_results(test_list)
            
        
    def print_results(self, test_list):
        #test_list - 0: login_test, 1: signup_test, 2: error_counter, 3:second_login_test 
        print("----------------------------------")   
        print ("Login Test: ", test_list[0])  
        if test_list[0] == False:
            print ("Signup Test: %s, error counter: %s"%(test_list[1], test_list[2]))  
            if test_list[1] == True:
               print("Second Login Test: %s"%test_list[3])   
               if test_list[3] == False:
                   print("Program didn't succeded on loggin in after created the account!")
            else:
                print("Program didn't succeded on creating account!")
        else:
            print("Account was already created. Login successful.")
        print("----------------------------------")


        
class LoginBot:
    def __init__(self, controller, browser):
        self.controller = controller
        self.browser = browser
        self.actions = ActionChains(self.browser)
    
    def do_login(self):
        self.browser.find_element_by_name("uname").send_keys(user_data["Username"])
        self.browser.find_element_by_name("pass").send_keys(user_data["Password"])
        
        confirm_login_button = self.browser.find_element_by_xpath('//*[@id="content"]/div[1]/form/table/tbody/tr[3]/td/input')
        self.actions.click(confirm_login_button)
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
    def __init__(self, controller, browser):
        self.controller = controller
        self.browser = browser
        self.actions = ActionChains(self.browser)
    
    def do_signup(self):
        go_signup_page_button = self.browser.find_element_by_xpath('//*[@id="content"]/div[2]/h3/a')
        self.actions.click(go_signup_page_button)
        self.actions.perform()
        
        self.browser.find_element_by_name("uuname").send_keys(user_data["Username"])
        self.browser.find_element_by_name("upass").send_keys(user_data["Password"])
        self.browser.find_element_by_name("upass2").send_keys(user_data["Password"])
        self.browser.find_element_by_name("urname").send_keys(user_data["Name"])
        self.browser.find_element_by_name("ucc").send_keys(user_data["Credit card"]) 
        self.browser.find_element_by_name("uemail").send_keys(user_data["E-Mail"])
        self.browser.find_element_by_name("uphone").send_keys(user_data["Phone number"])
        self.browser.find_element_by_name("uaddress").send_keys(user_data["Address"])
        

        confirm_signup_button = self.browser.find_element_by_name('signup')
        self.actions.click(confirm_signup_button)
        self.actions.perform()
        (could_signup, counter) = self.check_data()
        return could_signup, counter

        


    def check_data(self):
        counter = 0
        for i in range(1,8,1):
            data = self.browser.find_element_by_xpath('//*[@id="content"]/ul/li[%i]'%(i)).text
            data_type = data.split(":")[0]
            data_value = data.split(" ")[-1]
            #print(data_type, data_value, user_data[data_type])
            if data_value != user_data[data_type]:
                counter = counter + 1
                could_signup = False
        
        if counter == 0:
            could_signup = True

        self.go_back_login_page()

        return could_signup, counter


    def go_back_login_page(self):
        
        go_login_page_button = self.browser.find_element_by_xpath('//*[@id="content"]/p[2]/a')
        self.actions.click(go_login_page_button)
        self.actions.perform()

bot = ControllerBot()
bot() 

