from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast
from selenium.webdriver.support.ui import Select
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )



class nexus(object):
    
    def __init__(self, domain):
        self.domain = domain

        start  = self.domain.find(".com")
        self.dmn = self.domain[:start]
        
        self.f = open("nexusdialer_entry.txt")
        self.dte_list = ast.literal_eval(self.f.readline().strip())

        self.mnth1 = self.dte_list[0]
        self.mnth1_int = self.dte_list[1]
        self.yr1 = self.dte_list[2]

        self.mnth2 =  self.dte_list[3]
        self.mnth2_int = self.dte_list[4]
        self.yr2 = self.dte_list[5]

	self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()

        self.driver.implicitly_wait(60)
        self.driver.set_page_load_timeout(120)

  

    def __del__(self):
        self.driver.delete_all_cookies()
        self.driver.quit() 

   

    def login(self, username, password):
        self.driver.get("http://nexusdialer.com/websitesearch/emp/")
        self.driver.find_element_by_id("login").send_keys(username)
	self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_name("commit").click()

       

    def web_aud_over(self):
        web_aud_over_list = ast.literal_eval(self.f.readline().strip())

        self.driver.get("http://nexusdialer.com/websitesearch/emp/create_overview.php")
        select = Select(self.driver.find_element_by_name("sitename"))
	select.select_by_visible_text(self.dmn)
        
        dte = "%s/%s%s" %("01", self.mnth2_int, self.yr2)

        self.driver.find_element_by_id("datepicker").send_keys(dte)
        self.driver.find_element_by_id("search").send_keys(web_aud_over_list[0].replace("-", ""))
	self.driver.find_element_by_name("uploadedfile").send_keys(web_aud_over_list[1])

	self.driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()



def suparmain():
    obj = nexus("test.com")
    obj.login("jsingh", "india123")
    obj.web_aud_over()



if __name__=="__main__":
    suparmain()    

              



        
