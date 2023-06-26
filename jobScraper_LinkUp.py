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
    if website == 'LinkUp':
        jobs_list, num_listings = load_LinkUp_jobs_div(job_title, location, job_type)
        print('{} new job postings retrieved from {}.'.format(num_listings, website))
        return jobs_list, num_listings
    return [], 0

# ================== FUNCTIONS FOR LinkUp.COM =================== #


def load_LinkUp_jobs_div(job_title, location, job_type):
    getVars = {'sort': 'd'}
    url = ('https://search.linkup.com/search/results/' + job_title + "-jobs-in-" + location + "?" + urllib.parse.urlencode(getVars))
    job_list = []
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options)
    driver.get(url)
    driver.implicitly_wait(10)
    # extract job information
    job_elems = driver.find_elements(By.CSS_SELECTOR, 'div.col > div.job-listing > div.s12')
    for job in job_elems:
        job_dic = {}
        job_name = job.find_element(By.CSS_SELECTOR, "h4 a").text
        job_dic['job_name'] = job_name
        company_name = job.find_element(By.CSS_SELECTOR, "span").text
        job_dic['company_name'] = company_name
        job_key = "{}-{}".format(job_name ,company_name)
        job_dic['job_key'] = job_key
        job_link = job.find_element(By.CSS_SELECTOR, "h4 a").get_attribute("href")
        job_dic['job_link'] = job_link
        if job_link is not None:
            # set up web driver
            options = Options()
            options.add_argument('--headless=new')
            driver2 = webdriver.Chrome(options)
            driver2.get(job_link)  # visit job link
            driver2.implicitly_wait(10)  # wait for page to load
            job_description = driver2.find_element(By.CSS_SELECTOR, ".job-description").text
            job_dic['job_description'] = job_description
            driver2.quit()
        else:
            job_dic['job_description'] = ""
        job_list.append(job_dic)
    driver.quit()
    return job_list, len(job_list)


def find_job_offers_in_LinkUp(job_titles, job_locations, job_type):
    job_type = ''
    global job_data
    global isDoneSearching
    new_jobs_list = []
    for job_title in job_titles:
        for job_location in job_locations:
            new_jobs_list, num_listings = load_LinkUp_jobs_div(job_title, job_location, job_type)
            if num_listings > 0:
                job_data.extend(new_jobs_list)
    return job_data


def find_job_offers_async_in_LinkUp(job_titles, job_locations, job_type):
    global thread
    # Start a new thread for find_job_offers
    thread = threading.Thread(target=find_job_offers_in_LinkUp, args=(job_titles, job_locations, job_type))
    thread.start()


def get_job_offers_in_LinkUp():
    # Wait for the find_job_offers thread to complete
    global thread
    thread.join()  # type: ignore
    return job_data

# jobs_types = none


if __name__ == "__main__":
    jobs_list = find_jobs_from('LinkUp', 'cyber', 'miami', 'fulltime')
    print(jobs_list)
