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
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import re 
import urllib

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
	self.driver.implicitly_wait(120)
        self.driver.set_page_load_timeout(120)



    def __del__(self):
        self.driver.delete_all_cookies()
	self.driver.quit()
        self.display.stop()



    def ajax_complete(self, driver):
        try:
            time.sleep(0.5)
            return 0 == driver.execute_script("return jQuery.active")

        except WebDriverException:
            pass



    def wtng_fr_pg_ld(self):
        try:
            WebDriverWait(self.driver, 1000).until(self.ajax_complete,  "Timeout waiting for page to load")

        except WebDriverException:
            pass



    def mystrip(self, x):
        return str(x.get_text()).replace(",", "-").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()



    def login_fun(self):
        self.driver.get("https://secure.similarweb.com/account/login")
        self.driver.find_element_by_id("UserName").send_keys("kayakashyap213@gmail.com")
        self.driver.find_element_by_id("Password").send_keys("6Tresxcvbhy")
        self.driver.find_element_by_xpath("/html/body/section/div/div/div/form/fieldset/div/button").click()
        self.wtng_fr_pg_ld()
       


    def domain_and_date(self):
        self.driver.find_element_by_id("enter-website").clear() 
        self.driver.find_element_by_id("enter-website").send_keys(self.domain)
        self.wtng_fr_pg_ld()


    
    def web_aud_over(self):
        link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/overview?selectTrendLine=visits&aggDuration=monthly"
	link = link %(self.domain, self.dte)
	
	self.driver.get(link)       
        self.wtng_fr_pg_ld()

        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        total_desk_vist = soup.find("div", attrs={"class":"count c-blue ng-binding"})
        self.total_desk_vist = str(total_desk_vist.get_text()).replace(",", "-").strip()

	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div/div/a").click()  
        self.wtng_fr_pg_ld()

        time.sleep(60)

	self.web_aud_over_file = self.find_file("/tmp", "*.part")
        print self.web_aud_over_file

     
        
    def find_file(self, directory, exten):
        if exten == "*.part":
            direc_exet = "%s/%s" %(directory, exten)
               
            for fle in glob.glob(direc_exet):
                os.chmod(fle, 755)

                start = fle.find(".")
                exten_csv = "%s.xlsx" %(fle[:start])

                shutil.copy(fle, exten_csv)

                filename = filter(None, exten_csv.strip().split("/"))[-1]
                new_file = "%s/%s" %(self.directory, filename)

                shutil.move(exten_csv, new_file)
                shutil.move(fle, self.mydump)

                return new_file

        else:
            dir_file_csv = "%s/%s" %(directory, exten)

            for fle in glob.glob(dir_file_csv):
                os.chmod(fle, 755)

                filename = filter(None, fle.strip().split("/"))[-1]
                new_file = "%s/%s" %(self.directory, filename)

                shutil.move(filename, new_file)

                return new_file



    def web_geo(self):
        web_geo_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/geography"
	web_geo_link = web_geo_link %(self.domain, self.dte)

	self.driver.get(web_geo_link)
        self.wtng_fr_pg_ld()

	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div/form/a").click()
        self.wtng_fr_pg_ld()

        time.sleep(60)

	self.web_geo_file = self.find_file(os.getcwd(), "*.csv")
        print self.web_geo_file



    def web_audin(self):
        web_audn_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/interests"
        web_audn_link = web_audn_link  %(self.domain, self.dte)
       
        self.driver.get(web_audn_link)
        self.wtng_fr_pg_ld()

        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div/form[2]/a").click()        
        self.wtng_fr_pg_ld()

        time.sleep(60)

        self.web_audn_file = self.find_file(os.getcwd(), "*.csv")
        print self.web_audn_file
        


    def trafic_pd_org_all_src(self):
        trafic_pd_org_all_src_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/traffic/search?selectedTab=all"
        trafic_pd_org_all_src_link = trafic_pd_org_all_src_link %(self.domain, self.dte)
        
	self.driver.get(trafic_pd_org_all_src_link)
        self.wtng_fr_pg_ld()

 	page = self.driver.page_source

        tree = html.fromstring(page)

        trafic_pd_org_all_src_visit = tree.xpath("/html/body/div[2]/div[3]/section/div/div/div/div/div[2]/div/text()")
        trafic_pd_org_all_src_prcnt =  tree.xpath("/html/body/div[2]/div[3]/section/div/div/div/div/div[3]/div/strong/text()")

	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div[2]/div/div/div/div/div/form[2]/a").click()
        self.wtng_fr_pg_ld()

        time.sleep(30)

	self.trafic_pd_org_all_src_fle = self.find_file(os.getcwd(), "*.csv")       
        print trafic_pd_org_all_src_visit[0].strip()
	print self.trafic_pd_org_all_src_fle




    def trf_srch_grp(self):    
        start  = self.domain.find(".com")
        dmn = self.domain[:start]
 
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ dmn
       
        link2 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B2%2BexcludeBranded%3Bnotcontains%3B"+ dmn 

        link3 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B3%2BexcludeBranded%3Bnotcontains%3B"+ dmn
           
        self.trf_srch_grp_fle = []

        for lnk in [link1, link2, link3]:
            self.trf_srch_grp_1_2_3(lnk)
	    
        file_dir = "%s/%s" %(os.getcwd(), "*.csv")
	trf_srch_grp_fle_old  = glob.glob(file_dir)
	
	for fle in trf_srch_grp_fle_old:
            os.chmod(fle, 755)

	    filename = filter(None, fle.strip().split("/"))[-1]
	    new_file = "%s/%s" %(self.directory, filename)

	    shutil.move(filename, new_file)
	    self.trf_srch_grp_fle.append(new_file)

	print self.trf_srch_grp_fle



        
    def trf_srch_grp_1_2_3(self, grp_link):
        self.driver.get(grp_link)
        self.wtng_fr_pg_ld()

        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div[2]/div/div/div/div[2]/div/form/a").click()
        self.wtng_fr_pg_ld()

        time.sleep(60)




def supermain():
    obj = pro_similar("amazon.com", "12m")
    obj.login_fun()
    obj.domain_and_date()
    #obj.web_aud_over()
    #obj.web_geo()
    #obj.web_audin() 
    #obj.trafic_pd_org_all_src()
    obj.trf_srch_grp()
  
       

    
    


if __name__=="__main__":
    s = datetime.now()
    supermain()
    e = datetime.now()
    print [e - s]
