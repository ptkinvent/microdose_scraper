#!/usr/bin/python3

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class MicrodoseScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        # Log in
        self.driver.get(f'https://directory.microdose.buzz/login')
        self.driver.find_element_by_id('email').send_keys(self.email)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_css_selector('button.stk-button').click()
        print('Successfully logged in...')
        time.sleep(10)

    def scrape(self, page_num):
        self.driver.get(f'https://directory.microdose.buzz/companies?page_num={page_num}')
        print(f'Navigating to directory page {page_num}')
        time.sleep(10)
        elements = self.driver.find_elements_by_tag_name('td')
        if len(elements) == 0:
            print(f'===================== FAILED TO GET PAGE {page_num} =====================')
        names = [element.text.rstrip().replace('\n', ', ') for element in elements[0::4]]
        bios = [element.text.rstrip().replace('\n', ', ') for element in elements[1::4]]
        categories = [element.text.rstrip().replace('\n', ', ') for element in elements[2::4]]
        countries = [element.text.rstrip().replace('\n', ', ') for element in elements[3::4]]
        print(f'Successfully scraped {len(names)} companies')
        return names, bios, categories, countries


class CsvWriter:
    def __init__(self, fname):
        self.fname = fname
        with open(self.fname, mode='a') as f:
            writer = csv.writer(f)
            writer.writerow(['Names', 'Bios', 'Categories', 'Countries'])

    def write(self, names, bios, categories, countries):
        with open(self.fname, mode='a') as f:
            writer = csv.writer(f)
            for name, bio, category, country in zip(names, bios, categories, countries):
                writer.writerow([name, bio, category, country])


def main():
    email = os.environ.get('MICRODOSE_EMAIL')
    password = os.environ.get('MICRODOSE_PASSWORD')
    scraper = MicrodoseScraper(email=email, password=password)
    writer = CsvWriter(fname='microdose.csv')

    for page_num in range(145, 287):
        names, bios, categories, countries = scraper.scrape(page_num)
        writer.write(names, bios, categories, countries)

main()
