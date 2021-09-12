from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://aurora.umanitoba.ca/banprod/twbkwbis.P_GenMenu?name=homepage')
firstLink = driver.find_element_by_link_text('Enter Secure Area')
firstLink = driver.find_element_by_partial_link_text('Enter')
action = ActionChains(driver)
action.move_to_element(firstLink)
action.double_click()
action.perform()

userID = driver.find_element_by_id('UserID')
userID.send_keys('7838700')
psswrd = driver.find_element_by_id('PIN')
psswrd.send_keys('Qwerty1!')
psswrd.submit()
driver.implicitly_wait(3)

secondLink = driver.find_element_by_link_text('Enrolment & Academic Records')
secondLink = driver.find_element_by_partial_link_text('Enrolment')
action = ActionChains(driver)
action.move_to_element(secondLink)
action.double_click()
action.perform()
thirdLink = driver.find_element_by_link_text('Registration and Exams')
thirdLink = driver.find_element_by_partial_link_text('Registration')
action = ActionChains(driver)
action.move_to_element(thirdLink)
action.double_click()
action.perform()
driver.implicitly_wait(3)
fourth = driver.find_element_by_link_text('Student Detail Schedule')
fourth = driver.find_element_by_partial_link_text('Student Detail ')
action = ActionChains(driver)
action.move_to_element(fourth)
action.double_click()
action.perform()
driver.implicitly_wait(3)

form = driver.find_element_by_id('term_id')
form.send_keys('Fall 2021')
form.submit()

html = driver.page_source
soup = BeautifulSoup(html)
tables = soup.find_all("table", class_="datadisplaytable")
for i in range(len(tables)):
    if i % 2 == 0 and i >= 2 and i < 9:
        className = tables[i].contents[0].text

        t2 = tables[i].find_all('tr')
        waitList = t2[3].text
        print(className)
        print('\n' + waitList)

print(driver)
