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
should_exit = False


def find_jobs_from(website, job_title, location, job_type):
    if website == 'JobIsJob':
        jobs_list, num_listings = load_JobIsJob_jobs_div(
            job_title, location, job_type)
        print('{} new job postings retrieved from {}.'.format(
            num_listings, website))
        return jobs_list, num_listings
    return [], 0

# ================== FUNCTIONS FOR JobIsJob.COM =================== #


def load_JobIsJob_jobs_div(job_title, location, job_type):
    getVars = {'whatInSearchBox': job_title, 'whereInSearchBox': location}
    url = ('https://www.jobisjob.com/m/search?' +
           urllib.parse.urlencode(getVars))
    job_list = []
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options)
    driver.get(url)
    driver.implicitly_wait(3)

    # extract job information
    job_elems = driver.find_elements(By.CSS_SELECTOR, 'ul.list2 > li > a.item')
    for job in job_elems:
        if should_exit:
            return job_list, len(job_list)  # Exit the thread
        try:
            job_dic = {}
            job_name = job.find_element(
                By.CSS_SELECTOR, "div.item_data > span.title").text
            job_dic['job_name'] = job_name
            company_name = job.find_element(
                By.CSS_SELECTOR, 'div.item_data > span.subtitle').text
            job_dic['company_name'] = company_name
            job_key = "{}-{}".format(job_name, company_name)
            job_dic['job_key'] = job_key
            job_link = job.get_attribute("href")
            job_dic['job_link'] = job_link

            if job_link is not None:
                # set up web driver
                try:
                    options = Options()
                    options.add_argument('--headless=new')
                    driver2 = webdriver.Chrome(options)
                    driver2.get(job_link)  # visit job link
                    driver2.implicitly_wait(3)  # wait for page to load
                    job_description = driver2.find_element(
                        By.CSS_SELECTOR, "div.description > div.thebox > div").text
                    job_dic['job_description'] = job_description
                    driver2.quit()
                except:
                    job_dic['job_description'] = ""

            else:
                job_dic['job_description'] = ""
            job_list.append(job_dic)
        except:
            pass
    driver.quit()
    return job_list, len(job_list)


def find_job_offers_in_JobIsJob(job_titles, job_locations, job_type):
    job_type = ''
    global job_data
    global isDoneSearching
    new_jobs_list = []
    for job_title in job_titles:
        for job_location in job_locations:
            new_jobs_list, num_listings = load_JobIsJob_jobs_div(
                job_title, job_location, job_type)
            if num_listings > 0:
                job_data.extend(new_jobs_list)

    return job_data


def find_job_offers_thread_in_JobIsJob(job_titles, job_locations, job_type):
    global thread
    # Start a new thread for find_job_offers
    thread = threading.Thread(target=find_job_offers_in_JobIsJob, args=(
        job_titles, job_locations, job_type))
    thread.start()


def get_job_offers_in_JobIsJob(exit=False):
    # Wait for the find_job_offers_thread thread to complete
    global thread
    global job_data

    global should_exit
    should_exit = exit
    if thread.is_alive():
        thread.join()
    return job_data

# jobs_types = none


if __name__ == "__main__":
    jobs_list = find_jobs_from(
        'JobIsJob', 'data scientist', 'alabama', 'fulltime')
    print(jobs_list)
