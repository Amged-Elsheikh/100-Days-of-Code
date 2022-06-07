"""This file will contain data handler objects"""
import re
from selenium.webdriver.common.by import By


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
