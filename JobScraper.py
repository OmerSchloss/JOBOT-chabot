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


def find_jobs_from(website, job_title, location, desired_characs):
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

    if website == 'Indeed':
        # job_soup = load_indeed_jobs_div(job_title, location)
        # jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)
        jobs_list, num_listings = load_indeed_jobs_div(job_title, location)
        print('{} new job postings retrieved from {}.'.format(num_listings,
                                                              website))
        return jobs_list, num_listings

    if website == 'CWjobs':
        driver = initiate_driver(browser='chrome')
        job_soup = make_job_search(job_title, location, driver)
        jobs_list, num_listings = extract_job_information_cwjobs(
            job_soup, desired_characs)

        print('{} new job postings retrieved from {}.'.format(num_listings,
                                                              website))
        return jobs_list, num_listings

    return [], 0

    # save_jobs_to_excel(jobs_list, filename)


## ================== FUNCTIONS FOR INDEED.CO.UK =================== ##

def load_indeed_jobs_div(job_title, location):
    getVars = {'q': job_title, 'l': location,
               'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))

    job_list = []
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options)
    driver.get(url)

    # extract job information
    job_elems = driver.find_elements(
        By.CSS_SELECTOR, 'ul.jobsearch-ResultsList > li > div.cardOutline')

    for job in job_elems:
        job_dic = {}
        job_name = job.find_element(By.CSS_SELECTOR, ".jobTitle").text
        job_dic['job_name'] = job_name

        company_name = job.find_element(By.CSS_SELECTOR, '.companyName').text
        job_dic['company_name'] = company_name

        job_link = job.find_element(
            By.CSS_SELECTOR, "h2 a").get_attribute("href")
        job_dic['job_link'] = job_link

        if job_link is not None:
            # set up web driver
            options = Options()
            options.add_argument('--headless=new')

            driver2 = webdriver.Chrome(options)
            driver2.get(job_link)  # visit job link
            driver2.implicitly_wait(10)  # wait for page to load
            job_description = driver2.find_element(
                By.CSS_SELECTOR, "#jobDescriptionText").text
            job_dic['job_description'] = job_description

            driver2.quit()
        else:
            job_dic['job_description'] = ""

        job_list.append(job_dic)
    driver.quit()

    return job_list, len(job_list)


def load_indeed_jobs_info(job_title, location):
    getVars = {'q': job_title, 'l': location,
               'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.com/jobs?' +
           urllib.parse.urlencode(getVars))  # type: ignore
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(options)
    driver.get(url)
    # page = requests.get(url)
    job_elems = driver.find_elements(
        By.CSS_SELECTOR, 'ul.jobsearch-ResultsList li')
    # soup = BeautifulSoup(page.content, "html.parser")
    # job_soup = soup.find(id="resultsCol")
    # job_soup = soup.find(id="mosaic-jobResults")
    return job_elems


def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='jobsearch-SerpJobCard')

    cols = []
    extracted_info = []

    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    return title


def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company


def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.Indeed.co.uk/' + link
    return link


def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date


## ================== FUNCTIONS FOR CWJOBS.CO.UK =================== ##


def initiate_driver(browser):
    if browser == 'chrome':
        driver = webdriver.Chrome()
        return driver
    elif browser == 'firefox':
        driver = webdriver.Firefox()
        return driver
    elif browser == 'safari':
        driver = webdriver.Safari()
        return driver
    elif browser == 'edge':
        driver = webdriver.Edge()
        return driver
    return None


def make_job_search(job_title, location, driver):
    driver.get('https://www.cwjobs.co.uk/')

    # Select the job box
    job_title_box = driver.find_element_by_name('Keywords')

    # Send job information
    job_title_box.send_keys(job_title)

    # Selection location box
    location_box = driver.find_element_by_id('location')

    # Send location information
    location_box.send_keys(location)

    # Find Search button
    search_button = driver.find_element_by_id('search-button')
    search_button.click()

    driver.implicitly_wait(5)

    page_source = driver.page_source

    job_soup = BeautifulSoup(page_source, "html.parser")

    return job_soup


def extract_job_information_cwjobs(job_soup, desired_characs):

    job_elems = job_soup.find_all('div', class_="job")

    cols = []
    extracted_info = []

    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_cwjobs(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_cwjobs(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_cwjobs(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_cwjobs(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def extract_job_title_cwjobs(job_elem):
    title_elem = job_elem.find('h2')
    title = title_elem.text.strip()
    return title


def extract_company_cwjobs(job_elem):
    company_elem = job_elem.find('h3')
    company = company_elem.text.strip()
    return company


def extract_link_cwjobs(job_elem):
    link = job_elem.find('a')['href']
    return link


def extract_date_cwjobs(job_elem):
    link_elem = job_elem.find('li', class_='date-posted')
    link = link_elem.text.strip()
    return link


def find_job_offers(job_titles, job_locations):
    # job_data = scrape_indeed_jobs(job_titles[0], job_locations[0], 1)
    desired_characs = ['titles', 'companies', 'links', 'date_listed']
    global job_data
    global isDoneSearching

    new_jobs_list = []

    for job_title in job_titles:
        for job_location in job_locations:
            new_jobs_list, num_listings = find_jobs_from(
                'Indeed', job_title, job_location, desired_characs)
            # find_jobs_from('CWjobs', job_title, job_location, desired_characs)

            if (num_listings > 0):
                job_data.extend(new_jobs_list)

    return job_data


def find_job_offers_async(job_titles, job_locations):
    global thread
    # Start a new thread for find_job_offers
    thread = threading.Thread(target=find_job_offers,
                              args=(job_titles, job_locations))
    thread.start()


def get_job_offers():
    # Wait for the find_job_offers thread to complete
    global thread

    thread.join()  # type: ignore

    # Retrieve the job_data and process it
    # jobs_df = pd.DataFrame(job_data)

    return job_data


if __name__ == "__main__":
    desired_characs = ['titles', 'companies', 'links', 'date_listed']

    jobs_list = find_jobs_from(
        'Indeed', 'data scientist', 'london', desired_characs)
