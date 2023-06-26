import pandas as pd

import urllib.parse
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
job_data = []
isDoneSearching = True
thread = None


def find_jobs_from(website, job_title, location, job_type):
    if website == 'Google':
        jobs_list, num_listings = load_Google_jobs_div(job_title, location, job_type)
        print('{} new job postings retrieved from {}.'.format(num_listings, website))
        return jobs_list, num_listings
    return [], 0

# ================== FUNCTIONS FOR Google.COM =================== #


def load_Google_jobs_div(job_title, location, job_type):
    getVars = {'employment_type': job_type, 'location': location, 'q': job_title, 'sort_by': 'date'}
    url = ('https://careers.google.com/jobs/results/?' + urllib.parse.urlencode(getVars))
    job_list = []
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options)
    driver.get(url)
    driver.implicitly_wait(10)
    # extract job information
    job_elems = driver.find_elements(By.CSS_SELECTOR, 'ol.gc-p-results__results-list>li')
    for job in job_elems:
        job_dic = {}
        job_name = job.find_element(By.CSS_SELECTOR, "div.gc-card__header > h2.gc-card__title").text
        job_dic['job_name'] = job_name
        company_name = job.find_element(By.CSS_SELECTOR, "ul.gc-job-tags > li.gc-job-tags__team > span").text
        job_dic['company_name'] = company_name
        job_key = "{}-{}".format(job_name ,company_name)
        job_dic['job_key'] = job_key
        job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        job_dic['job_link'] = job_link

        if job_link is not None:
            # set up web driver
            options = Options()
            options.add_argument('--headless=new')
            driver2 = webdriver.Chrome(options)
            driver2.get(job_link)  # visit job link
            driver2.implicitly_wait(10)  # wait for page to load
            job_description = driver2.find_element(By.CSS_SELECTOR, ".gc-job-detail__section--description").text
            job_dic['job_description'] = job_description
            driver2.quit()
        else:
            job_dic['job_description'] = ""
        job_list.append(job_dic)
    driver.quit()
    return job_list, len(job_list)


def find_job_offers_in_Google(job_titles, job_locations, job_type):
    if job_type == 'fulltime':
        job_type = 'FULL_TIME'
    elif job_type == 'temporary':
        job_type = 'TEMPORARY'
    elif job_type == 'internship':
        job_type = 'INTERN'
    elif job_type == 'parttime':
        job_type = 'PART_TIME'
    else:
        job_type = ''
    global job_data
    global isDoneSearching
    new_jobs_list = []
    for job_title in job_titles:
        for job_location in job_locations:
            new_jobs_list, num_listings = load_Google_jobs_div(job_title, job_location, job_type)
            if num_listings > 0:
                job_data.extend(new_jobs_list)

    return job_data


def find_job_offers_async_in_Google(job_titles, job_locations, job_type):
    global thread
    # Start a new thread for find_job_offers
    thread = threading.Thread(target=find_job_offers_in_Google, args=(job_titles, job_locations, job_type))
    thread.start()


def get_job_offers_in_Google():
    # Wait for the find_job_offers thread to complete
    global thread
    thread.join()  # type: ignore
    return job_data



# jobs_types = [FULL_TIME, TEMPORARY, PART_TIME, INTERN]


if __name__ == "__main__":
    jobs_list = find_jobs_from('Google', 'Cyber', 'Alabama', 'FULL_TIME')
    print(jobs_list)
