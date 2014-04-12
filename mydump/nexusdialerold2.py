from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast
from selenium.webdriver.support.ui import Select
import logging
import time
import os
import re 

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )



class nexus(object):

    def __init__(self, domain):
        self.di = os.getcwd()
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

        self.my_month = {"Jan":"Jan", "Feb":"Feb", "Mar":"March",
                         "Apr":"April", "May":"May", "Jun":"June",
                         "Jul":"July", "Aug":"Aug", "Sep":"Sep" ,
                         "Oct":"Oct", "Nov":"Nov", "Dec":"Dec"}

        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Firefox()
        self.driver.maximize_window()

        self.driver.implicitly_wait(60)
        self.driver.set_page_load_timeout(120)



    def __del__(self):
        self.driver.delete_all_cookies()
        self.driver.quit()



    def line_extracton(self):
        self.web_aud_over_list = ast.literal_eval(self.f.readline().strip())
        self.web_aud_geo_list = ast.literal_eval(self.f.readline().strip())
        self.web_aud_aud_list = ast.literal_eval(self.f.readline().strip())
        self.trf_src_op_all_list = ast.literal_eval(self.f.readline().strip())
        self.trf_srch_grp1_list = ast.literal_eval(self.f.readline().strip())
        self.trf_srch_grp2_list = ast.literal_eval(self.f.readline().strip())
        


    def login(self, username, password):
        self.driver.get("http://nexusdialer.com/websitesearch/emp/")
        self.driver.find_element_by_id("login").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_name("commit").click()



    def web_aud_over(self):
        web_aud_over_list = self.web_aud_over_list

        self.driver.get("http://nexusdialer.com/websitesearch/emp/create_overview.php")
        select = Select(self.driver.find_element_by_name("sitename"))
        select.select_by_visible_text(self.dmn)

        dte = "%s/0%s/%s" %("01", self.mnth2_int, self.yr2)

        self.driver.find_element_by_id("datepicker").send_keys(dte)
        self.driver.find_element_by_id("search").send_keys(web_aud_over_list[0].replace("-", ""))
   
        fi = "%s/%s" %(self.di, web_aud_over_list[-1])
        self.driver.find_element_by_id("uploadedfile").send_keys(fi)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()

        

    def web_aud_geo(self):
        web_aud_geo_list = self.web_aud_geo_list

	self.driver.get("http://nexusdialer.com/websitesearch/emp/create_geography.php")
	select = Select(self.driver.find_element_by_name("sitename"))
	select.select_by_visible_text(self.dmn)

	dte = "0%s/%s/%s" %(self.mnth2_int, "01", self.yr2)
	self.driver.find_element_by_id("datepicker").send_keys(dte)
        self.driver.find_element_by_id("datepicker").send_keys(Keys.RETURN)

	fi = "%s/%s" %(self.di, web_aud_geo_list[0])
	self.driver.find_element_by_id("uploadedfile").send_keys(fi)

	self.driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()



    def web_aud_aud(self):
        web_aud_aud_list = self.web_aud_aud_list
  
        self.driver.get("http://nexusdialer.com/websitesearch/emp/create_audience.php")
        select = Select(self.driver.find_element_by_name("sitename"))
        select.select_by_visible_text(self.dmn)
  
        dte = "0%s/%s/%s" %(self.mnth2_int, "01", self.yr2)
        self.driver.find_element_by_id("datepicker").send_keys(dte)
  
        fi = "%s/%s" %(self.di, web_aud_aud_list[0])
        self.driver.find_element_by_id("uploadedfile").send_keys(fi)
        self.driver.find_element_by_id("datepicker").send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()



    def trf_src_op_all(self):
        trf_src_op_all_list = self.trf_src_op_all_list

        self.driver.get("http://nexusdialer.com/websitesearch/emp/searchkeyword.php")

        select = Select(self.driver.find_element_by_name("sitename"))
	select.select_by_visible_text(self.dmn)

        select = Select(self.driver.find_element_by_name("month"))
        select.select_by_visible_text(self.my_month[self.mnth2])

        select = Select(self.driver.find_element_by_name("year"))
        select.select_by_visible_text(self.yr2)

        self.driver.find_element_by_name("totalvisit").send_keys(trf_src_op_all_list[-1].replace(",", ""))
     
        fi = "%s/%s" %(self.di, trf_src_op_all_list[0])
        self.driver.find_element_by_id("uploadedfile").send_keys(fi)

	self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/input").click()



    def trf_srch_grp2(self):
        trf_srch_grp2_list = self.trf_srch_grp2_list

	self.driver.get("http://nexusdialer.com/websitesearch/emp/search2words.php")
	
	select = Select(self.driver.find_element_by_name("sitename"))
        select.select_by_visible_text(self.dmn)

	select = Select(self.driver.find_element_by_name("month"))
	select.select_by_visible_text(self.my_month[self.mnth2])

	select = Select(self.driver.find_element_by_name("year"))
	select.select_by_visible_text(self.yr2)

        self.driver.find_element_by_name("totalvisit").send_keys(trf_srch_grp2_list[-1].replace(",", ""))

	fi = "%s/%s" %(self.di, trf_srch_grp2_list[0])
	self.driver.find_element_by_id("uploadedfile").send_keys(fi)

	self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/input").click()
       
         

def suparmain():
    obj = nexus("test.com")
    obj.login("jsingh", "india123")
    obj.line_extracton()
    #obj.web_aud_over()
    #obj.web_aud_geo()
    #obj.web_aud_aud()
    #obj.trf_src_op_all()
    obj.trf_srch_grp2()
    

    time.sleep(120)

                             

if __name__=="__main__":
    suparmain()
    
