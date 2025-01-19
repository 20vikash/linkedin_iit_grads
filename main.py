# type: ignore

import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from read_env import *
import time
import csv

def write_to_csv(data, file_name="linkedin_data_2.csv"):
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if file.tell() == 0:
            writer.writerow(["Name", "Company", "Post"])
        
        writer.writerow(data)

def scroll_alumni_page(driver):
    count = 0

    while True:
        count += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if count == 20:
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

    name_div = soup.find("div", class_="pwvoXWdekMutuFrtXlPtIrLjWHgnWkwvzdVVis")
    name = name_div.find("h1").text
    
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
                    print("Name: {}, Company: {}, post: {}".format(name, company, post))
                    write_to_csv([name.strip(), company.strip(), post.strip()])

        else:
            continue

service = Service(executable_path="./chromedriver")
driver = uc.Chrome(service=service)

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

time.sleep(10)

alumni_page_url = get_iit_madras_url()
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
