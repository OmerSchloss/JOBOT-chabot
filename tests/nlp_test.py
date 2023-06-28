import sys
sys.path.append('../JOBOT')

from nlp import is_positive_response, is_negative_response, want_to_start_job_search, process_answer_job_title, process_answer_location, process_answer_job_type, get_short_description

test_cases = [
    "Yes, I am interested.",
    "No, I'm not interested.",
    "I want to start my job search.",
    "I am looking for a software engineer position.",
    "I prefer working in Tel Aviv.",
    "I am interested in a full-time position.",
    "I am a recent graduate looking for an internship.",
    "This is a long description for testing purposes.",
    "Yes, I'm excited to start my job search!",
    "No, I'm not interested at the moment.",
    "I'm ready to explore new career opportunities.",
    "I'm searching for a software developer role.",
    "I prefer working in Tel Aviv or Jerusalem.",
    "I'm specifically looking for full-time positions.",
    "I want to secure an internship in the field of finance.",
    "This is a long description with multiple sentences. It should be summarized in the short description.",
    "Absolutely!",
    "Not really, but thanks for asking.",
    "I'm a recent graduate and I'm actively seeking employment.",
    "I aspire to be a data scientist.",
    "Remote work is my preferred choice.",
    "I'm interested in contract-based roles.",
    "I have expertise in web development.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ullamcorper tellus vitae ligula pretium efficitur.",
    "I'm not sure yet, still exploring my options.",
    "I'm looking for part-time positions.",
    "I want to work in the healthcare industry.",
    "I'm open to relocation for the right opportunity.",
    "I'm not interested in an internship.",
    "I'm seeking a senior-level position.",
    "I'm interested in both technical and non-technical roles.",
    "I want to work in a startup environment.",
    "I have a background in marketing and sales.",
    "I'm interested in positions related to artificial intelligence.",
    "I prefer a flexible work schedule.",
    "I'm interested in a temporary job for the summer.",
    "I have experience in customer service.",
]

# Perform the tests and collect the results
results = {
    "Positive Response": [],
    "Negative Response": [],
    "Want to Start Job Search": [],
    "Job Titles": [],
    "Locations": [],
    "Job Types": [],
    "Short Descriptions": [],
}

for test_case in test_cases:
    results["Positive Response"].append(is_positive_response(test_case))
    results["Negative Response"].append(is_negative_response(test_case))
    results["Want to Start Job Search"].append(
        want_to_start_job_search(test_case))
    results["Job Titles"].append(process_answer_job_title(test_case))
    results["Locations"].append(process_answer_location(test_case))
    results["Job Types"].append(process_answer_job_type(test_case))
    results["Short Descriptions"].append(get_short_description(test_case))

# Analyze the results and calculate the grades
grades = {
    "Positive Response": round((sum(results["Positive Response"]) / 3) * 100) if results["Positive Response"] else 0,
    "Negative Response": round((sum(results["Negative Response"]) / 5) * 100) if results["Negative Response"] else 0,
    "Want to Start Job Search": round((sum(results["Want to Start Job Search"]) / 3) * 100) if results["Want to Start Job Search"] else 0,
    "Job Titles": round(((sum(title != [] for title in results["Job Titles"]) - 24) / 8) * 100) if results["Job Titles"] else 0,
    "Locations": round((sum(location != "" for location in results["Locations"]) / len(results["Locations"])) * 100) if results["Locations"] else 0,
    "Job Types": round((sum(job_type != "" for job_type in results["Job Types"]) / 8) * 100) if results["Job Types"] else 0,
}

# Calculate the overall grade
overall_grade = round(sum(grades.values()) / len(grades))

# Send the analysis with the grades
analysis = f"Grade Breakdown:\n"
for key, value in grades.items():
    analysis += f"{key}: {value}%\n"
analysis += f"\nOverall Grade: {overall_grade}%"

print(analysis)
