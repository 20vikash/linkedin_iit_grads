# LinkedIn Alumni Data Scraper

This project is a Python-based script designed to scrape IIT alumni profile data (Name, Company, and Job Title) from LinkedIn. It is specifically tailored for educational and research purposes, complying with LinkedIn's terms of use.

## Features

- **Login Automation:** Automates login to LinkedIn using Selenium and `undetected_chromedriver`.
- **Alumni Data Extraction:** Scrapes alumni names, companies, and job titles from a specified alumni page.
- **CSV Output:** Saves the extracted data to a CSV file (`linkedin_data.csv`).
- **Manual CAPTCHA Handling:** Includes a pause (`time.sleep(10)`) to allow manual CAPTCHA resolution during execution.
- **Scalable Design:** Structured for potential enhancements like proxy rotation and IP address masking.
