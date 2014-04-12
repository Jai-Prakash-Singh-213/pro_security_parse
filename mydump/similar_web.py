import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import time
from pyvirtualdisplay import Display
from selenium.webdriver.common.action_chains import ActionChains


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class secure_web(object):

    def __init__(self, username, password, loginlink):
        
        self.display = Display()
        self.display.start()
        self.username = username
	self.password = password
	self.loginlink = loginlink

        fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList",2)
	fp.set_preference("browser.download.manager.showWhenStarting",False)
	fp.set_preference("browser.download.dir", os.getcwd())
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv/xls")
        #fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.ms-exce')

	self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(30)



    def __del__(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
        self.display.stop()



    def login(self):
        self.driver.get(self.loginlink)
	elem = self.driver.find_element_by_id("UserName")
	elem.send_keys(self.username)
	elempass = self.driver.find_element_by_id("Password")
	elempass.send_keys(self.password)
	elem.send_keys(Keys.RETURN)



    def set_site_and_date(self, site, dt):
        elemwbst = self.driver.find_element_by_id("enter-website")
	elemwbst.clear()
	elemwbst.send_keys(site)

        xpthformont = "/html/body/div[2]/div[2]/div[5]/div/div/input"
        elmmnt = self.driver.find_element_by_xpath(xpthformont)
        hov = ActionChains(self.driver).move_to_element(elmmnt)
        hov.perform()
        elmmnt.click()

        elmmnt = self.driver.find_element_by_xpath(dt)
	elmmnt.click()



    def dwnload_csv(self, pth):
        elem_csv = self.driver.find_element_by_xpath(pth)
	elem_csv.click()



    def load_time(self):
        try:
            WebDriverWait(self.driver, 1000).until(self.ajax_complete,  "Timeout waiting for page to load")
        except WebDriverException:
            pass



    
    def ajax_complete(self, driver):
        try:
            time.sleep(0.5)
            return 0 == driver.execute_script("return jQuery.active")
        except WebDriverException:
            pass






def supermain():
    username = "kayakashyap213@gmail.com"
    password =  "6Tresxcvbhy"
    loginlink = "https://secure.similarweb.com/account/login"

    obj1 = secure_web(username, password, loginlink)
    obj1.login()

    webst = "amazon.com"
    date_dict = {"month" : "/html/body/div[2]/div[2]/div[5]/div/div/div/div/button", 
                 "three_month" : "/html/body/div[2]/div[2]/div[5]/div/div/div/div/button[2]",
                 "six_month" : "/html/body/div[2]/div[2]/div[5]/div/div/div/div/button[3]",
                 "twlv_month" : "/html/body/div[2]/div[2]/div[5]/div/div/div/div/button[4]"}

    web_aud_dwn_link = "/html/body/div[2]/div[3]/section/div/div/div[2]/div/div/a"
    
    for pos , dt in date_dict.items():
        obj1.set_site_and_date(webst, dt)
        obj1.load_time()
        obj1.dwnload_csv(web_aud_dwn_link)
        obj1.load_time()




if __name__=="__main__":
    supermain()
