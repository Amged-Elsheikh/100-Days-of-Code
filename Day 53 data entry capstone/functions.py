from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from house_data_handler import *


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