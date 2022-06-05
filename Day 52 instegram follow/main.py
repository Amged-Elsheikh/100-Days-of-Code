import os
from time import sleep

import dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

"""One of the marketing strategies in SNS for getting the attention of targeted customers is to mark some pages doing something relevant to what you are doing or your potential competitors.
By following all the followers of that page, you are sure that you have made a free ad to your new page/business for the people that might seem interested in your product.
"""

dotenv.load_dotenv()

# Downlaod your brower's 'webdriver', unzip the file and write it's directory
chromedrive_dir = "C://Users//amged//developer//chromedriver.exe"


class InstaManager:
    def __init__(self,):
        # initialize the webdriver
        chrome_driver = chromedrive_dir
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        # Open the browser
        self.driver.get("https://www.instagram.com/")

    def login(self):
        # WRITE YOUR EMAIL ADDRESS AND PASSWORD
        email_address = os.environ.get("MY_EMAIL")
        password = os.environ.get("META_PASSWORD")
        # sleep for two second, giving the browser time to open the webpage
        sleep(2)
        # Login process
        email = self.driver.find_element_by_name("username")
        email.send_keys(email_address)
        password_entry = self.driver.find_element_by_name("password")
        password_entry.send_keys(password)
        password_entry.send_keys(Keys.RETURN)
        # Sleep for 5 seconds, to give the server time to load
        sleep(5)

    def open_popup(self, page, number_of_expansion=30):
        # Open the Page you want to follow it's followers
        self.driver.get(f"https://www.instagram.com/{page}")
        sleep(3)
        # Open the followers pop-up window
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        sleep(3)
        # Expand the pop up window to get as much followers as possible
        try:
            self._expand_popup(number_of_expansion)
        except ElementClickInterceptedException:
            print("Could n't login")
            raise

    def _expand_popup(self, number_of_expansion=30):
        pop_list = self.driver.find_element_by_css_selector('.isgrP')
        for _ in range(number_of_expansion):
            # Scroll to the end of the list using Java Script command
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", pop_list)
            sleep(0.8)

    def follow_followers(self):
        """This method will click the follow button for all accounts that appears in the popup window
        """
        # Get hold of all opened accounts
        accounts = self.driver.find_elements_by_css_selector(
            ".isgrP li button")
        for account in accounts:
            # Make sure that the account is not already followed to avoid error
            if account.text.lower() == 'follow':
                account.click()
                # Wait for one second before following the next account so that the server can process the request smoothly
                sleep(1)

    def unfollow_followers(self):
        """This method will unfollow all the followers of page of your choice.
        Not recommended at all.
        """
        accounts = self.driver.find_elements_by_css_selector(
            ".isgrP li button")
        for account in accounts:
            if account.text == 'Following':
                account.click()
                sleep(1)
                self.driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div/div[3]/button[1]').click()
                sleep(1)

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    insta_bot = InstaManager()
    insta_bot.login()
    pages_to_check = input(
        'Enter the ID of all pages youwant to follow their followers separated by by single space " "\n')
    pages_to_check = pages_to_check.split(" ")
    for page in pages_to_check:
        insta_bot.open_popup(page)
        # Use follow or unfollow
        insta_bot.follow_followers()
        # To unfollow
        # insta_bot.unfollow_followers()
    insta_bot.close()
