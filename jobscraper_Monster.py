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


def find_jobs_from(website, job_title, location, job_type, desired_characs):
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'Indeed' or 'CWjobs')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .xls file called 'results.xls'
    """

    if website == 'Monster':
        jobs_list, num_listings = load_Monster_jobs_div(job_title, location, job_type)
        print('{} new job postings retrieved from {}.'.format(num_listings, website))
        return jobs_list, num_listings

    return [], 0

# ================== FUNCTIONS FOR Monster.COM =================== #


def load_Monster_jobs_div(job_title, location, job_type):
    getVars = {'q': job_title, 'where': location, 'et': job_type,
               'fromage': 'last', 'sort': 'date'}
    url = ('https://www.monster.com/jobs/search?' + urllib.parse.urlencode(getVars))

    job_list = []
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options)
    driver.get(url)
    driver.implicitly_wait(10)  # wait for page to load

    # extract job information
    job_elems = driver.find_elements(By.CSS_SELECTOR, 'ul.iJeGss>li.cSkSaC>div.gFeVEp')

    for job in job_elems:
        job_dic = {}
        job_name = job.find_element(By.CSS_SELECTOR, ".fmZqNQ").text
        job_dic['job_name'] = job_name

        company_name = job.find_element(By.CSS_SELECTOR, '.eBtdTX').text
        job_dic['company_name'] = company_name

        job_link = job.find_element(
            By.CSS_SELECTOR, "h3 a").get_attribute("href")
        job_dic['job_link'] = job_link

        if job_link is not None:
            try:
                # set up web driver
                options = Options()
                options.add_argument('--headless=new')

                driver2 = webdriver.Chrome(options)
                driver2.get(job_link)  # visit job link
                driver2.implicitly_wait(10)  # wait for page to load
                job_description = driver2.find_element(
                    By.CSS_SELECTOR, "div.crOoVX").text
                job_dic['job_description'] = job_description

                driver2.quit()
            except:
                job_dic['job_description'] = ""
        else:
            job_dic['job_description'] = ""

        job_list.append(job_dic)
    driver.quit()

    return job_list, len(job_list)


def find_job_offers(job_titles, job_locations, job_type):
    # job_data = scrape_indeed_jobs(job_titles[0], job_locations[0], 1)
    desired_characs = ['titles', 'companies', 'links', 'date_listed']
    global job_data
    global isDoneSearching

    new_jobs_list = []

    for job_title in job_titles:
        for job_location in job_locations:
            new_jobs_list, num_listings = find_jobs_from(
                'Monster', job_title, job_location, job_type, desired_characs)
            # find_jobs_from('CWjobs', job_title, job_location, desired_characs)

            if (num_listings > 0):
                job_data.extend(new_jobs_list)

    return job_data


def find_job_offers_async(job_titles, job_locations, job_type):
    global thread
    # Start a new thread for find_job_offers
    thread = threading.Thread(target=find_job_offers,
                              args=(job_titles, job_locations, job_type))
    thread.start()


def get_job_offers():
    # Wait for the find_job_offers thread to complete
    global thread

    thread.join()  # type: ignore

    return job_data


if __name__ == "__main__":
    desired_characs = ['titles', 'companies', 'links', 'date_listed']
    jobs_list,num = find_jobs_from('Monster', 'Data scientist', 'Alabama', 'FULL_TIME', desired_characs)
    print(jobs_list)


