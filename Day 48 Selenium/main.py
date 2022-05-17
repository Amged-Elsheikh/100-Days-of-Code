from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os

chrome_driver = "C://Users//amged//developer//chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)

################################ Python website ################################
# driver.get("https://www.python.org/")
# events_data = driver.find_elements_by_css_selector('.event-widget li')

# events = {i: {'date': sel.find_element_by_tag_name('time').text,
#               "name": sel.find_element_by_tag_name('a').text}
#               for i, sel in enumerate(events_data)}

# print(events)
# driver.quit()

################################ Wikipedia ################################
# driver.get("https://en.m.wikipedia.org/wiki/Main_Page")
# articals_count = driver.find_element_by_css_selector("#articlecount a")
# print(articals_count.text)

# driver.quit()

################################ Input practice #############################
# driver.get("http://secure-retreat-92358.herokuapp.com/")
# fname = driver.find_element_by_name("fName")
# fname.send_keys("Amged")
# lname = driver.find_element_by_name("lName")
# lname.send_keys("Elsheikh")
# email = driver.find_element_by_name("email")
# email.send_keys("A@gmail.com")
# button = driver.find_element_by_css_selector("button")
# button.click()

################################ Cookie game #############################
driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie = driver.find_element_by_css_selector("#bigCookie")
i = 0
while True:
    try:
        cookie.click()
        i+=1
        if i%1000==0:
            purchase_counter = 10
            while purchase_counter>=0:
                try:
                    item = driver.find_elements_by_class_name("enabled")[-1]
                    upgrade = driver.find_element_by_css_selector("#upgrade0")
                    item.click()
                    upgrade.click()
                    purchase_counter -= 1
                except:
                    purchase_counter=-1
    except:
        driver.quit()
        break