from selenium import webdriver

from functions import *
from house_data_handler import *


if __name__ == '__main__':
    # Write your webdriver directory
    chrome_driver = "C://Users//amged//developer//chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)
    # Filter the apartments by the desired creiteria and past the full url here
    yolo_link = "https://home.yolo-japan.com/en/tokyo/list?priceTo=95&room=2,3&dateBuild=30&property_type_id=3102,3101&buildingEquipment=23201,20101&perPage=50&page=1"
    # Fill the google form link
    # The given form will be closed soon. please create your own form to collect the data
    form_link = "https://forms.gle/MkNrwYRsZJzHWt7t5"
    # Open Yolo
    open_yolo(driver, yolo_link)
    # Create the dataframe (This will take several minutes)
    df = create_apartments_df(driver)
    # Start filling goolge form
    # When filling a the form, edit all Xpathes inside the function, to match yours
    fill_form(driver, df, form_link)
