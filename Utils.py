import pandas as pd

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

def create_demo_job_list():
    # Create the DataFrame
    jobs_df = pd.DataFrame(job_data)

    # Display the DataFrame
    print(jobs_df)

    return jobs_df


def create_demo_user():
    # # Create a dictionary to hold the data
    # data = {'Question': questions}
    # # Add the sample answers as separate columns
    # for i in range(len(sample_answers)):
    #     data[f'Answer {i + 1}'] = sample_answers[i]
    # # Create a DataFrame
    # df = pd.DataFrame(data)
    # # Display the DataFrame
    # print(df)
    # return df

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

    # Print the resulting DataFrame
    print(df)

    return df

if __name__ == '__main__':
    create_demo_user()


