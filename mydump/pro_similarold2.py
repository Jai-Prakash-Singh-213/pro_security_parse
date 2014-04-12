from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
import os 
from bs4 import BeautifulSoup
from lxml import html
import time
import glob
import os, sys, stat
import shutil
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class pro_similar(object):

    def __init__(self, domain, dte):
        self.domain = domain
	self.dte = dte

        display = Display()
	self.display = display.start()

	fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
	fp.set_preference("browser.download.dir", os.getcwd())
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

	self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.maximize_window()
	self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(60)



    def __del__(self):
        self.driver.delete_all_cookies()
        time.sleep(4)
	self.driver.quit()
        self.display.stop()



    def mystrip(self, x):
        return str(x.get_text()).replace(",", "-").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()



    def login_fun(self):
        self.driver.get("https://secure.similarweb.com/account/login")
        self.driver.find_element_by_id("UserName").send_keys("kayakashyap213@gmail.com")
        self.driver.find_element_by_id("Password").send_keys("6Tresxcvbhy")
        self.driver.find_element_by_xpath("/html/body/section/div/div/div/form/fieldset/div/button").click()
       

    def domain_and_date(self):
        self.driver.find_element_by_id("enter-website").clear() 
        self.driver.find_element_by_id("enter-website").send_keys(self.domain)
        


    def web_aud_over(self):
        link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/overview?selectTrendLine=visits&aggDuration=monthly"
	link = link %(self.domain, self.dte)
	
	self.driver.get(link)
	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div/div/a").click()
  
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        total_desk_vist = soup.find("div", attrs={"class":"count c-blue ng-binding"})
        self.total_desk_vist = str(total_desk_vist.get_text()).replace(",", "-").strip()
        
	self.find_file("/tmp", "*.part")

     
        
    def find_file(self, directory, exten):
        if exten == "*.part":
            direc_exet = "%s/%s" %(directory, exten)

            for fle in glob.glob(direc_exet):
                start = fle.find(".")
                exten_csv = "%s.xlsx" %(fle[:start])
	        shutil.copy2(fle, exten_csv)
                os.chmod(exten_csv, stat.S_IRWXG)
            
        print self.total_desk_vist
 



def supermain():
    obj = pro_similar("amazon.com", "12m")
    obj.login_fun()
    obj.domain_and_date()
    obj.web_aud_over() 




if __name__=="__main__":
    supermain()
