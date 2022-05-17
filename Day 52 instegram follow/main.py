from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep
import random
import os
import dotenv

dotenv.load_dotenv()

class InstaManager:
    
    def __init__(self,):
        chrome_driver = "C://Users//amged//developer//chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        self.driver.get("https://www.instagram.com/")
        
    def login(self):
        email_address = os.environ.get("MY_EMAIL")
        password = os.environ.get("META_PASSWORD")
        sleep(2)
        email = self.driver.find_element_by_name("username")
        email.send_keys(email_address)
        password_entry = self.driver.find_element_by_name("password")
        password_entry.send_keys(password)
        password_entry.send_keys(Keys.RETURN)
        sleep(3)
        
    def open_popup(self, page, number_of_expansion=30):
        # Got to the Page
        self.driver.get(f"https://www.instagram.com/{page}")
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div').click()
        sleep(3)
        # Expand the pop up
        self._expand_popup(number_of_expansion)
        pass
        
    def follow_followers(self):
        accounts = self.driver.find_elements_by_css_selector(".isgrP li button")
        for account in accounts:
            # try:
            if account.text=='Follow':
                account.click()
                sleep(0.5)
            # except ElementClickInterceptedException:
            #     cancel_button = self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[2]')
            #     cancel_button.click()
            #     sleep(1)
    
    def unfollow_followers(self):
        accounts = self.driver.find_elements_by_css_selector(".isgrP li button")
        for account in accounts:
            if account.text=='Following':
                account.click()
                sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[1]').click()
                sleep(1)
        
        
    def _expand_popup(self, number_of_expansion=30):
        pop_list = self.driver.find_element_by_css_selector('.isgrP')
        for _ in range(number_of_expansion):
        # Scroll to the end of the list using Java Script command
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_list)
            sleep(1)
        
    def close(self):
        self.driver.close()
    
    def random_sleeper(self):
        return random.randrange(1,3) + random.randrange(-100,100)/100
    
if __name__ == "__main__":
    insta_bot = InstaManager()
    insta_bot.login()
    pages_to_check = ['arsenal', ]
    for page in pages_to_check:
        insta_bot.open_popup(page)
        # Use follow or unfollow
        # insta_bot.follow_followers()
        # To unfollow
        insta_bot.unfollow_followers()
    insta_bot.close()