from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from read_env import *
import time

def scroll_alumni_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    return driver.page_source

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

email = get_email()
password = get_password()

driver.get("https://linkedin.com")

signin_element = driver.find_element(By.CLASS_NAME, "nav__button-secondary")
signin_element.click()

email_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

email_field.send_keys(email)
password_field.send_keys(password)

signin_button = driver.find_element(By.CLASS_NAME, "btn__primary--large")
signin_button.click()

alumni_page_url = get_iit_delhi_url()
driver.get(alumni_page_url)

alumunus = scroll_alumni_page(driver)
print(alumunus)
