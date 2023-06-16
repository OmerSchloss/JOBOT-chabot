import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_indeed_jobs(query, location, num_pages):
    base_url = "https://www.indeed.com/jobs"
    job_data = []
    
    for page in range(num_pages):
        params = {
            "q": query,
            "l": location,
            "start": page * 10  # Each page displays 10 job offers
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(base_url, params=params, headers=headers)

        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            job_elements = soup.select(".jobsearch-SerpJobCard")
            for job_element in job_elements:
                title_element = job_element.select_one(".jobtitle")
                title = title_element.text.strip() if title_element else ""
                
                company_element = job_element.select_one(".company")
                company = company_element.text.strip() if company_element else ""
                
                location_element = job_element.select_one(".location")
                location = location_element.text.strip() if location_element else ""
                
                description_element = job_element.select_one(".summary")
                description = description_element.text.strip() if description_element else ""

                job_offer = {
                    "Job name": title,
                    "Job Company": company,
                    "Job location": location,
                    "Job description": description
                }

                job_data.append(job_offer)
        
        else:
            print(f"Failed to retrieve job data for page {page+1}. Status code:", response.status_code)

    return job_data

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
    #job_data = scrape_indeed_jobs(job_titles[0], job_locations[0], 1)
    jobs_df = pd.DataFrame(job_data)

    # Display the DataFrame
    print(jobs_df)

    return jobs_df
