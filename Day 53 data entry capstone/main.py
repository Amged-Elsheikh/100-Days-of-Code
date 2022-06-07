import re
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


# Create data handling classes
class House:
    def __init__(self, house):
        # Get houses tags
        self.house = house
        # house type and name
        self.full_name = self.house.find_element(
            by=By.TAG_NAME, value='h5').text
        # house Type
        self.building_type = re.match(
            'Apartment\s[a-zA-Z]+', self.full_name).group(0)
        # house name
        self.building_name = self.full_name.replace(
            f'{self.building_type }', "")
        # Get address and building age
        self.address, self.age = self.house.find_elements(
            by=By.CSS_SELECTOR, value='.txt-info span')
        self.address = self.address.text
        # check if newly built
        try:
            self.age = int(
                re.search('[0-9]+', self.age.text.split('/')[1]).group())
        except:
            self.age = 0
        # get a list of vaccant apartment in the building
        self.apartments = house.find_elements(
            by=By.CSS_SELECTOR, value='.property-list .item-right')


class apartment:
    def __init__(self, apartment):
        self.apartment = apartment
        self.apartment_link = self.apartment.find_element(
            by=By.CSS_SELECTOR, value='a').get_attribute('href')
        self.apartment_id = re.search(
            '[0-9]*$', self.apartment_link).group(0)
        # Rent
        self.monthly_payment = self.apartment.find_element(
            by=By.CSS_SELECTOR, value='.price').text
        self.monthly_payment = int(sum(
            [int(re.sub("[^0-9.]", '', i)) for i in self.monthly_payment.split('/') if i]))
        # One time payment
        self.otp = self.apartment.find_element(
            by=By.CSS_SELECTOR, value='.w-40').text.split('\n')[1]
        self.otp = int(sum([int(re.sub("[^0-9.]", '', i))
                       for i in self.otp.split('/')]))

        self.apartment_text = self.apartment.text
        self.floor = int(re.search(
            '[0-9]+', re.search('[0-9a-zA-Z]*\sfloor', self.apartment_text).group()).group())
        self.area = float(
            re.search('[0-9.]+m2', self.apartment_text).group().replace('m2', ''))
        self.apartment_type = re.search(
            'floor [0-9]+[A-Z]', self.apartment_text).group().replace('floor ', '')


def open_yolo(driver, yolo_link):
    driver.get(yolo_link)
    sleep(5)
    try:
        # Close the langauge pop-up menu if it appears
        driver.find_element(by=By.CSS_SELECTOR,
                            value='.modal-body ul li').click()
    except:
        pass
    # Change the view
    # YOLO webpage is a dynamic one, the code need full screen window (1080p) or small text to scrape the data
    driver.maximize_window()
    driver.find_element(
        by=By.XPATH, value='/html/body/div/div/div/div[2]/div[2]/section[3]/div/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/button[2]').click()


def create_apartments_df(driver):
    # Initialize the dataframe
    columns = ['ID', 'Name', 'Type', 'Built In', 'Address', 'Floor Number',
               'Room Type', 'Area', 'URL', 'One time payment', 'Monthly Payment']
    df = pd.DataFrame(columns=columns)
    # Keep looping in all pages
    while True:
        houses = driver.find_elements(
            by=By.CSS_SELECTOR, value='.property-wrapper')
        for house in houses:
            house = House(house)
            for apartment in house.apartments:
                apartment = apartment(apartment)
                data = {'ID': apartment.apartment_id,
                        'Name': house.building_name,
                        'Type': house.building_type,
                        'Built In': 2022 - house.age,
                        'Address': house.address,
                        'Floor Number': apartment.floor,
                        'Room Type': apartment.apartment_type,
                        'Area': apartment.area,
                        'URL': apartment.apartment_link,
                        'One time payment': apartment.otp,
                        'Monthly Payment': apartment.monthly_payment}
                df = df.append(data, ignore_index=True)
        # Check if this was the last page
        next_button = driver.find_element(
            by=By.XPATH, value='/html/body/div/div/div/div[2]/div[2]/section[3]/div/div[2]/div/div/div[1]/div[2]/div/button[2]')
        if next_button.is_enabled():
            next_button.click()
            sleep(5)
        else:
            break
    return df


def fill_form(driver, df: pd.DataFrame, form_link):
    columns = list(df.columns)
    for i in range(len(df)):
        # go to the google form
        driver.get(form_link)
        sleep(1)
        apartment_id = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[0]])
        building_name = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[1]])
        building_type = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[2]])
        built_in = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[3]])
        address = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea').send_keys(df.loc[i, columns[4]])
        floor = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[5]])
        room_type = driver.find_element(
            by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[6]])
        area = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[7]])
        link = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[8]])
        otp = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[9]])
        rent = driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(df.loc[i, columns[10]])
    # Submit the form
        driver.find_element(
            by=By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div').click()
        sleep(1)


if __name__ == '__main__':
    # Write your webdriver directory
    chrome_driver = "C://Users//amged//developer//chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)
    # Filter the apartments by the desired creiteria and past the full url here
    yolo_link = "https://home.yolo-japan.com/en/tokyo/list?priceTo=95&room=2,3&dateBuild=30&property_type_id=3102,3101&buildingEquipment=23201,20101&perPage=50&page=1"
    # Write the google form link
    form_link = "https://forms.gle/MkNrwYRsZJzHWt7t5"
    # Open Yolo
    open_yolo(driver, yolo_link)
    df = create_apartments_df(driver)
    fill_form(driver, df, form_link)
