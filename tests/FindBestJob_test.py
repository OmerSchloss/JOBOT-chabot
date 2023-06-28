import sys
sys.path.append('../JOBOT')

import pandas as pd
from FindBestJob import find_the_best_job

# Define the questions and sample answers
questions = [
    "What is your preferred job title or role?",
    "What industry or field are you interested in?",
    "How many years of experience do you have in this field?",
    "What are your specific skills or areas of expertise?",
    "Are you looking for full-time, part-time, or freelance opportunities?",
    "What is your preferred location for the job?",
    "Are you open to remote work or do you prefer on-site positions?",
    "What is your desired salary range?",
    "Are there any specific companies or organizations you would like to work for?",
    "What level of education or certifications do you possess?",
    "Are there any specific job benefits or perks you value?"
]

optional_answers = [
    ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Data Engineer"],
    ["Technology", "Finance", "Healthcare", "E-commerce"],
    ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"],
    ["Python programming", "Statistical analysis", "Machine learning algorithms", "Data visualization", "Big data technologies (e.g., Hadoop, Spark)"],
    ["Full-time", "Part-time", "Freelance"],
    ["San Francisco, CA", "New York, NY", "London, UK", "Bangalore, India"],
    ["Open to remote work", "Prefer on-site positions"],
    ["$60,000 - $80,000", "$80,000 - $100,000", "$100,000 - $120,000", "Above $120,000"],
    ["Google", "Amazon", "Microsoft", "Facebook"],
    ["Bachelor's degree in Computer Science", "Master's degree in Data Science", "Ph.D. in Statistics", "Certifications in machine learning (e.g., TensorFlow, scikit-learn)"],
    ["Flexible work hours", "Health insurance", "Stock options", "Professional development opportunities"]
]

users_answers = [
    ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Data Engineer"],
    ["Technology", "Finance", "Healthcare", "E-commerce"],
    ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"],
    ["Python programming", "Statistical analysis", "Machine learning algorithms", "Data visualization"],
    ["Full-time", "Part-time", "Freelance", "Freelance"],
    ["San Francisco, CA", "New York, NY", "London, UK", "Bangalore, India"],
    ["Open to remote work", "Prefer on-site positions", "Prefer on-site positions", "Prefer on-site positions"],
    ["$60,000 - $80,000", "$80,000 - $100,000", "$100,000 - $120,000", "Above $120,000"],
    ["Google", "Amazon", "Microsoft", "Facebook"],
    ["Bachelor's degree in Computer Science", "Master's degree in Data Science", "Ph.D. in Statistics", "Certifications in machine learning (e.g., TensorFlow, scikit-learn)"],
    ["Flexible work hours", "Health insurance", "Stock options", "Professional development opportunities"]
]

# Example job data
job_data = [
    {
        'job_name': 'Software Engineer',
        'job_Company': 'ABC Tech',
        'job_key': 'aa-bb',
        'job_location': 'New York',
        'job_description': 'We are seeking a skilled software engineer to join our dynamic team. In this role, you will be responsible for designing and developing high-quality software solutions. You should have a strong background in software development and be familiar with various programming languages and frameworks. If you are passionate about coding and enjoy working on challenging projects, we would love to hear from you!',
        'job_link': "www.fake1.com"
    },
    {
        'job_name': 'Data Analyst',
        'company_name': 'XYZ Analytics',
        'job_key': 'bb-cc',
        'job_location': 'San Francisco',
        'job_description': 'Join our team as a data analyst and play a crucial role in extracting valuable insights from large datasets. As a data analyst, you will be responsible for collecting, cleaning, and analyzing data to identify trends and patterns. Proficiency in SQL, Python, and data visualization tools is required. If you have a strong analytical mindset and enjoy working with data, we invite you to apply!',
        'job_link': "www.fake2.com"

    },
    {
        'job_name': 'Marketing Manager',
        'company_name': 'Marketing Inc.',
        'job_key': 'cc-dd',
        'job_location': 'Chicago',
        'job_description': 'Looking for an experienced marketing manager to lead our marketing efforts. In this role, you will develop and execute marketing strategies to promote our products and services. You should have a solid understanding of digital marketing techniques, including SEO, social media marketing, and email campaigns. Excellent communication and leadership skills are essential. If you are a creative thinker with a passion for marketing, we want to hear from you!',
        'job_link': "www.fake3.com"

    },
]

def create_demo_job_list():
    # Create the DataFrame
    jobs_df = pd.DataFrame(job_data)
    return jobs_df


def create_demo_user():
    # Create a dictionary with questions as keys and empty lists as values
    data_dict = {question: [] for question in questions}

    # Append the answers for each user to the respective question list
    for user_answers in zip(*users_answers):
        for i, answer in enumerate(user_answers):
            data_dict[questions[i]].append(answer)

    # Create the DataFrame using the dictionary
    df = pd.DataFrame(data_dict)
    # Combine user's answers into a single input string
    df['Combined_Answers'] = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    return df

if __name__ == '__main__':
    df_QA = create_demo_user()
    jobs_df = create_demo_job_list()
    new_offer, job_link, job_key =find_the_best_job(df_QA,jobs_df)
    print("\n\n\n")
    print("best job offer:\n ", new_offer.replace("<br>","\n"))
    print("best job link: ", job_link)


