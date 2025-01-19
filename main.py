# type: ignore

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from read_env import *
import time

def scroll_alumni_page(driver):
    count = 0

    while True:
        count += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if count == 10:
            break
    
    return driver.page_source

def get_company_and_post(job):
    company_name = ""
    job_post = ""

    span_text = job.find("span")

    if span_text.find_parent("a"):
        company_name = span_text.text

        posts = job.find("div", class_="pvs-entity__sub-components")
        titles = posts.find_all("span")
        for title in titles:
            if title.find_parent("a"):
                job_post = title.text
                break
            
    else:
        job_post = span_text.text

        companies_span = job.find("span", class_="t-14")
        company_name = companies_span.find("span").text

    
    return (company_name, job_post)
    
def write_data(html):
    soup = BeautifulSoup(html, "lxml")
    
    headings = soup.find_all("div", class_="iRQlucHUKclOVnnLzGCMMOriIYNHADAA")

    for heading in headings:
        inner_heading = heading.find("div", class_="QvYTNNlszJhnEXEKkmnBOtkhIHmILXpwOMOo")
        text = inner_heading.h2.find("span").text

        if text == "Experience":
            experience_data = heading.find_next_sibling("div", "UQjKXOxyggyZUXDaNIZsmGMhVepkFdnMfYPxuUPfdY")
            jobs = experience_data.find_all("li")

            for job in jobs:
                company, post = get_company_and_post(job)
                if len(post) > 1:
                    print("Company: {}, post: {}".format(company, post))

        else:
            continue

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

soup = BeautifulSoup(alumunus, "lxml")

people = soup.find_all("div", class_="org-people-profile-card__profile-info")

for person in people:
    link = person.find("a")

    if link:
        link = link["href"]

        driver.get(link)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "iRQlucHUKclOVnnLzGCMMOriIYNHADAA"))
            )

            page_html = driver.page_source
            write_data(page_html)

        except Exception as e:
            pass
        
    else:
        continue
