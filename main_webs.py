import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
from bs4 import BeautifulSoup
import requests
import pandas
from pandas import DataFrame
import csv, sys
import streamlit as st
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

#URL = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
#XPATH = "//*[@class='ui-mainview-block eventpath-wrapper']"
#TIMEOUT = 20

st.title("Test Selenium")
#st.markdown("You should see some random Football match text below in about 21 seconds")



non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
contact_link = []
contact_name = []
contact_job_title = []
contact_location = []
contact_about = []
contact_experience = []
contact_email = []
contact_phone_number = []
contact_education = []
key_words = []
def main():
    
    #print("Please key in your Linkedin User ID")
    #usr = input()
    usr = st.text_input("Please key in your Linkedin User ID")
    if usr == None:
        return
    st.write("user pass")
    #usr = "hazlanhamdan89@gmail.com"
    #print("Please key in your Linkedin Password")
    pwd = st.text_input("Please key in your Linkedin Password", type='password')
    if pwd == None:
        return
    st.write("pwd pass")
    #pwd = input()
    #pwd = "hazlan100189"

      
    print('Please key in your key word. (word and/or word and/or word ... etc)')
    'data science and power BI or anaplan'
    words = st.text_input('Please key in your key word. (word and/or word and/or word ... etc)')
    if words == None:
        return
    st.write("words pass")
    
    print("How many profile do you want to scrape?")
    number = st.number_input("How many profile do you want to scrape?")
    if number == 0.00:
        return
    st.write("number pass")
    #sys.exit()
    #driver = webdriver.Chrome(executable_path='chromedriver.exe')
    
    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )
    #driver.get(URL)
    #driver = webdriver.Firefox(executable_path="geckodriver.exe")
    #driver.get(url)
    driver.get('https://www.linkedin.com')
    time.sleep(1)

    # Log into LinkedIn
    username = driver.find_element_by_id('session_key')
    username.send_keys(usr)

    time.sleep(0.5)

    password = driver.find_element_by_id('session_password')
    password.send_keys(pwd)

    time.sleep(0.5)

    log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    log_in_button.click()

    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
     
    # to search
    #query = 'site:linkedin.com/in/ AND ' + listToStr + 'AND "Malaysia"'
    query = 'site:linkedin.com/in/ AND ' + words 
     
    for j in search(query, tld="com", num=number, stop=number, pause=2):
        print(j)
        driver.get(j)
        
        hasLoadMore = True
        count = 0
        while hasLoadMore:
            time.sleep(1)
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if count > 1:
                    hasLoadMore = False
                else:
                    count = count + 1
            except:
                hasLoadMore = False
        
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        
        contact_link.append(j)

        soup_name = soup.find('h1', { "class": "text-heading-xlarge inline t-24 v-align-middle break-words" })
        if soup_name == None:
            contact_name.append("N/A")
        else:
            contact_name.append(soup_name.text.strip())
            print(soup_name.text.strip())
        
        soup_job_title = soup.find('div', { "class": "text-body-medium break-words"})
        if soup_job_title == None:
            contact_job_title.append("N/A")
        else:
            contact_job_title.append(soup_job_title.text.strip())
            print(soup_job_title.text.strip().translate(non_bmp_map))

        time.sleep(1)
        exp = soup.find_all("section")
        sect_exp = []
        for i in exp:
            soup_exp = i.find('div',{"id":"experience"})
            print(soup_exp)
            if soup_exp != None:
                print(i)
                details_exp = i.find_all('li',{"class":"artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
                for x,z in enumerate(details_exp):
                    m = z.find_all('span',{"aria-hidden":"true"})
                    for y in m:
                        print(y.text.strip().translate(non_bmp_map))
                        sect_exp.append(str(x) + ":" + y.text.strip().translate(non_bmp_map))
        contact_experience.append(sect_exp)

        time.sleep(1)
        exp = soup.find_all("section")
        sect_edu = []
        for j in exp:
            soup_edu = j.find('div',{"id":"education"})
            print(soup_edu)
            if soup_edu != None:
                print(j)
                details_edu = j.find_all('li',{"class":"artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
                #print(details_edu)
                for x,z in enumerate(details_edu):
                    m = z.find_all('span',{"aria-hidden":"true"})
                    for y in m:
                        print(y.text.strip().translate(non_bmp_map))
                        sect_edu.append(str(x) + ":" + y.text.strip().translate(non_bmp_map))
        contact_education.append(sect_edu)  
        
        time.sleep(1)
        abt = soup.find_all("section")
        about = 0
        for k in abt:
            soup_about = k.find('div',{"id":"about"})
            print(soup_about)
            if soup_about != None:
                print(k)
                details_about = k.find('div',{"class":"pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"})
                about = details_about.find('span',{"aria-hidden":"true"})
                print(about.text.strip().translate(non_bmp_map))
                #contact_about.append(about.text.strip().translate(non_bmp_map))
                #test = 1
        if about == 0:
            contact_about.append("N/A")
        else:
            contact_about.append(about.text.strip().translate(non_bmp_map))
        
        #soup_location = soup.find('li', {"class":"t-16 t-black t-normal inline-block"})
        soup_location = soup.find('div', {"class":"pb2 pv-text-details__left-panel"})
        
        if soup_location == None:
            contact_location.append("N/A")
        else:
            contact_location.append(soup_location.text.strip())
            print(soup_location.text.strip())
        
        soup_phone_number = soup.find('span', {"class":"t-14 t-black t-normal"})

        if soup_phone_number == None:
            contact_phone_number.append("N/A")
        else:
            contact_phone_number.append(soup_phone_number.text.strip())
            print(soup_phone_number.text.strip())

        soup_email_1 = soup.find('selection', {"class":"pv-contact-info__contact-type ci-email"})

        if soup_email_1 != None:
            soup_email_2 = soup_email_1.find('a', {"class":"pv-contact-info__contact-link t-14 t-black t-normal"})

        if soup_email_1 == None:
            contact_email.append("N/A")
        else:
            contact_email.append(soup_email_2.text.strip())
            print(soup_email_2.text.strip())
        time.sleep(2)

    data = {'link': contact_link,
            'name': contact_name,
            'job_title':contact_job_title,
            'location':contact_location,
            'phone_number':contact_phone_number,
            'email':contact_email,
            'experience':contact_experience,
            'about':contact_about,
            'education':contact_education}

    #print(data)

    print([len(v) for v in data.values()])
    time.sleep(1)
    df = DataFrame(data, columns = ['link',
                                    'name',
                                    'job_title',
                                    'location',
                                    'email',
                                    'phone_number','experience','about','education'])

    df.to_csv('data.csv')
    driver.quit()
    print("Job Done!!!")
    st.write("Job Done!!!")

if __name__ == "__main__":
    main()
