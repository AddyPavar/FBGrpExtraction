import sys
import configparser
import json,urllib.request
import time
import csv

from selenium import webdriver  ## WebScraping Framework
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup   ## Scraping html

options = Options()                                                 ## Firefox Options
options.set_preference("dom.webnotifications.enabled", False)       ## Disable Browser notification prompt

configParser = configparser.RawConfigParser()                       ## ConfigParser for reading Config File
configFilePath = r'fb.conf'                                         ## Source config file
configParser.read(configFilePath)                                   ## Read Config file
# access_token = configParser.get('APITOKEN', 'access_token')         
# apiver = configParser.get('APITOKEN', 'apiver')
email = configParser.get('Creds', 'username')                       ## Read Username
pwd = configParser.get('Creds', 'password')                         ## Read Password

# baseurl = "https://{0}/{1}/".format(host,apiver)

def getMembers(group_id='me',output='console'):
    driver = webdriver.Firefox(executable_path='geckodriver.exe', firefox_options=options)  ## Initializing Browser
    baseurl ="https://www.facebook.com/groups/{0}/members".format(group_id)                 ## Target URL
    driver.get(baseurl)                                                                     ## Calling facebook
    driver.find_element_by_id("email").send_keys(email)                                     ## Send Username
    driver.find_element_by_id("pass").send_keys(pwd)                                        ## Send Password
    driver.find_element_by_id("loginbutton").send_keys(u'\ue007')                           ## Login
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "groupsMemberBrowserContent")))
                                                                                            ## Wait page to load
    while True:
        # preOffset = driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            ## Scroll Content
        # if driver.find_element_by_class_name("fbProfileBrowserList expandedList fbProfileBrowserNoMoreItems"):
        if driver.find_elements_by_xpath("//*[@class='fbProfileBrowserList expandedList fbProfileBrowserNoMoreItems']"):
            break
        # print(driver.execute_script("return document.body.scrollHeight;"))
    html= driver.page_source                                                                ## Get HTML Source
    soup = BeautifulSoup(html, 'lxml')                                                      ## Parse to BS4
    tag=soup.find('div', {'id': 'groupsMemberSection_recently_joined'})                     ## Find desire DIV if you are member
    
    if tag == None:
        tag = soup.find('div', {'id': 'groupsMemberSection_all_members'})                   ## Find desire DIV if you are Admin

    tag = tag.find('div', {'class': 'fbProfileBrowserListContainer'})                       ## Get Profile container
    # for achr in tag.finAll('a'):
    #     print(achr.string)
    with open('members.csv', 'w', encoding="utf-8", newline='') as csvfile:                 ## Initialize the CSV

        # Column of csv file
        column_name = ['Name', 'ProfileURL']                                                ## Define Column Name and Profile URL
        writer = csv.DictWriter(csvfile, fieldnames=column_name)                            
        writer.writeheader()                                                                ## Header Write
    
        for link in tag.findAll('a'):                                                       ## Find each Anchor tag contains Name
            link = link
            if link.string != None:
                writer.writerow({
                    'Name': link.string,
                    'ProfileURL': link["href"]
                })


getMembers(group_id=sys.argv[1])                                                            ## Send system-argument