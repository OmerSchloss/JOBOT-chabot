import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
from urllib.parse import urlencode
from selenium import webdriver
from urllib.parse import urlencode


def get_indeed_search_url(keyword, location, offset=0):
    parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
    return "https://il.indeed.com/jobs?" + urlencode(parameters)


def scrape_job_details(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()

    content = BeautifulSoup(html, 'lxml')
    jobs_list = []

    for post in content.select('.job_seen_beacon'):
        try:
            data = {
                "job_title": post.select('.jobTitle')[0].get_text().strip(),
                "company": post.select('.companyName')[0].get_text().strip(),
                "location": post.select('.companyLocation')[0].get_text().strip(),
                "date": post.select('.date')[0].get_text().strip()
            }
            print(data)
            jobs_list.append(data)
        except IndexError:
            continue

    return jobs_list


if __name__ == "__main__":
    current_url = get_indeed_search_url('Data Scientist', 'rehovot')
    print(current_url)
    job_data = scrape_job_details(current_url)
    print(job_data)

# Example job data
job_data = [
    {
        'Job name': 'Software Engineer',
        'Job Company': 'ABC Tech',
        'Job location': 'New York',
        'Job description': 'We are seeking a skilled software engineer to join our dynamic team. In this role, you will be responsible for designing and developing high-quality software solutions. You should have a strong background in software development and be familiar with various programming languages and frameworks. If you are passionate about coding and enjoy working on challenging projects, we would love to hear from you!'
    },
    {
        'Job name': 'Data Analyst',
        'Job Company': 'XYZ Analytics',
        'Job location': 'San Francisco',
        'Job description': 'Join our team as a data analyst and play a crucial role in extracting valuable insights from large datasets. As a data analyst, you will be responsible for collecting, cleaning, and analyzing data to identify trends and patterns. Proficiency in SQL, Python, and data visualization tools is required. If you have a strong analytical mindset and enjoy working with data, we invite you to apply!'
    },
    {
        'Job name': 'Marketing Manager',
        'Job Company': 'Marketing Inc.',
        'Job location': 'Chicago',
        'Job description': 'Looking for an experienced marketing manager to lead our marketing efforts. In this role, you will develop and execute marketing strategies to promote our products and services. You should have a solid understanding of digital marketing techniques, including SEO, social media marketing, and email campaigns. Excellent communication and leadership skills are essential. If you are a creative thinker with a passion for marketing, we want to hear from you!'
    },
    # Add more job entries as needed
]


def generate_job_offers(job_titles, job_locations):
    # job_data = scrape_indeed_jobs(job_titles[0], job_locations[0], 1)
    jobs_df = pd.DataFrame(job_data)

    # Display the DataFrame
    print(jobs_df)

    return jobs_df
