from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
import os 
from bs4 import BeautifulSoup
from lxml import html
import time
import glob
import shutil
import os, sys, stat
import time 
import logging
import profile
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )



class pro_similar(object):

    def __init__(self, domain, dte):
        self.domain = domain
	self.dte = dte
     
        self.mydump = "mydump_pro_similatr"
        try:
            os.makedirs(self.mydump)
        except:
            pass

        self.directory = "dirpro%s" %(time.strftime("%d%m%Y"))
        try:
            os.makedirs(self.directory)
        except:
            pass

        display = Display()
	self.display = display.start()

	fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
	fp.set_preference("browser.download.dir", os.getcwd())
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

	self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.maximize_window()
	self.driver.implicitly_wait(180)
        self.driver.set_page_load_timeout(180)



    def __del__(self):
        self.driver.delete_all_cookies()
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
	self.web_aud_over_file = self.find_file("/tmp", "*.part")
        print self.web_aud_over_file

     
        
    def find_file(self, directory, exten):
        if exten == "*.part":
            direc_exet = "%s/%s" %(directory, exten)
               
            for fle in glob.glob(direc_exet):
                os.chmod(fle, 755)
                start = fle.find(".")
                exten_csv = "%s.xlsx" %(fle[:start])
	        #os.copyfile(fle, exten_csv)
                shutil.copy(fle, exten_csv)
                filename = filter(None, exten_csv.strip().split("/"))[-1]
                new_file = "%s/%s" %(self.directory, filename)
                #os.renames(exten_csv, new_file)
                shutil.move(exten_csv, new_file)
                shutil.move(fle, self.mydump)
                return new_file

        else:
            dir_file_csv = "%s/%s" %(directory, exten)
             
            for fle in glob.glob(dir_file_csv):
                filename = filter(None, fle.strip().split("/"))[-1]
                new_file = "%s/%s" %(self.directory, filename)
                os.chmod(fle, 755)
                #os.renames(filename, new_file)
                shutil.move(filename, new_file)
                return new_file



    def web_geo(self):
        web_geo_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/geography"
	web_geo_link = web_geo_link %(self.domain, self.dte)

	self.driver.get(web_geo_link)
	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div/form/a").click()

        time.sleep(4)        
	self.web_geo_file = self.find_file(os.getcwd(), "*.csv")
        print self.web_geo_file

        

def supermain():
    obj = pro_similar("amazon.com", "12m")
    obj.login_fun()
    obj.domain_and_date()
    obj.web_aud_over()
    obj.web_geo()
    


if __name__=="__main__":
    s = datetime.now()
    supermain()
    e = datetime.now()
    print [e - s]
