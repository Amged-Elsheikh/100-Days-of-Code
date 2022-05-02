from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import os
import dotenv
import re

dotenv.load_dotenv()

"""
LinkedIn do not wannt bots in their website
"""


class linkedinDriver():
    chrome_driver = "C://Users//amged//developer//chromedriver.exe"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver)
        self.login()
        
    @staticmethod
    def random_sleeper(self):
        # get a random sleep interval
        return random.randrange(1,8) + random.randrange(-100,100)/100
        
    def login(self):
        self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        # Log in
        sleep(self.random_sleeper)
        email = self.driver.find_element_by_id("username")
        email.send_keys(os.environ.get("MY_EMAIL"))
        sleep(self.random_sleeper)
        password = self.driver.find_element_by_id("password")
        password.send_keys(os.environ.get("LINKEDIN_PASSWORD"))
        sleep(self.random_sleeper)
        password.send_keys(Keys.RETURN)
        sleep(self.random_sleeper)
        
    def process_jobs(self, url):
        self.driver.get(url)
        self.counter = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/header/div[1]/small").text
        print(self.counter)
        self.counter = int(re.match("[0-9]+", self.counter)[0])
        
        pages_number = int(self.counter/25) + 1
        for page in pages_number:
            try:
                print(f"Scrapping page {page}")
                
                jobs = driver.find_elements_by_css_selector(".jobs-search-results__list-item")
                for job in jobs:
                    self.save_job(job)
                    # Sleep between jobs
                    sleep(self.random_sleeper)
                # Sleep between pages
                self.sleep(10)
                self.driver.find_elements_by_css_selector(f"li button [aria-label=Page {page}]").click()
            except:
                print("Exception appeared")
                break
        
    def save_job(self, job):
        # Select the job
        job.click()
        # click save button
        driver.find_element_by_css_selector(".jobs-save-button").click()
        
    def close(self):
        self.driver.close()
        

if __name__=="__main__":
    data_science_entry_japan = "https://www.linkedin.com/jobs/search/?f_AL=true&f_E=2&f_JT=F&geoId=101355337&keywords=data%20science&location=Japan"
    driver = linkedinDriver()
    try:
        driver.login()
        driver.process_jobs(data_science_entry_japan)
    except:
        pass
    driver.close()
    