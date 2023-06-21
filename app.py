import random
# from chatbot import CB
from flask import Flask, render_template, request
import pandas as pd
from FindBestJob import find_the_best_job
from JobScraper import find_job_offers_async, get_job_offers
import nlp

# import webview

# app = Flask(__name__)
app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Conversation flow questions
questions = [
    "What is your preferred job title or role?",
    "What is your preferred location for the job?",

    "What industry or field are you interested in?",
    "How many years of experience do you have in this field?",
    "What are your specific skills or areas of expertise?",
    "Are you looking for full-time, part-time, or freelance opportunities?",
    "Are you open to remote work or do you prefer on-site positions?",
    "What is your desired salary range?",
    "Are there any specific companies or organizations you would like to work for?",
    "What level of education or certifications do you possess?",
    "Are there any specific job benefits or perks you value?"
]

conversation_topics = [
    "resume",
    "networking",
    "interview preparation",
    "career development",
    "work-life balance"
]

# Track conversation state
last_step = None
current_step = None
current_question = None
job_search_started = False
answers = []
askedQuestions = []
job_titles = None
job_locations = None


def get_next_question():
    # Retrieve the next question based on the conversation flow
    # If there are no more questions, return "start job search"
    if len(questions) > 0:
        return questions.pop(0)
    else:
        return "Would you like to start the job search?"


def get_random_conversation_topic():
    # Retrieve a random conversation topic
    return random.choice(conversation_topics)


@app.route("/chatbot")
def home():
    return render_template("index.html")


@app.route("/reset")
def reset_conversation():

    global last_step
    global current_step
    global current_question
    global job_search_started
    global answers
    global questions
    global askedQuestions
    global job_titles
    global job_locations

    # Conversation flow questions
    questions = [
        "What is your preferred job title or role?",
        "What is your preferred location for the job?",

        "What industry or field are you interested in?",
        "How many years of experience do you have in this field?",
        "What are your specific skills or areas of expertise?",
        "Are you looking for full-time, part-time, or freelance opportunities?",
        "Are you open to remote work or do you prefer on-site positions?",
        "What is your desired salary range?",
        "Are there any specific companies or organizations you would like to work for?",
        "What level of education or certifications do you possess?",
        "Are there any specific job benefits or perks you value?"
    ]

    answers = []
    askedQuestions = []
    last_step = None
    current_step = None
    current_question = None
    job_search_started = False
    job_titles = []
    job_locations = []

    return "Conversation has been reset. You can now start a new conversation."


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = 'well'  # str(CB.get_response(userText))

    global last_step  # None
    global current_step  # None
    global current_question  # None
    global job_search_started
    global questions
    global answers
    global askedQuestions
    global job_titles
    global job_locations

    if current_step is None:
        # Welcome message and first question to start the conversation
        welcome_message = "Hello! I'm here to assist you with your job search. Would you like to start?"
        current_step = "start"
        return welcome_message

    if current_step == "start":
        if userText is not None and (nlp.is_positive_response(userText.lower())):
            # User wants to start the job search
            current_step = "questions"
            current_question = get_next_question()
            return current_question
        elif userText is not None and (nlp.is_negative_response(userText.lower())):
            if (last_step != "conversation"):
                # User wants to engage in a conversation about advice and job-related topics
                current_step = "conversation"
                topic = get_random_conversation_topic()
                return f"Sure! Let's talk about {topic}. What would you like to know or discuss?"
            current_step = "conversation"
        else:
            return "I'm sorry, I didn't understand your response. Could you please answer with 'yes' or 'no' in a different way? For example, you can say 'absolutely' or 'not at the moment'."

    if current_step == "questions":

        if current_question == "What is your preferred job title or role?":
            job_titles = nlp.process_answer_job_title(userText)
            print(job_titles)
            if job_titles == []:
                return "I didn't catch any job title, please try again."

        if current_question == "What is your preferred location for the job?":
            job_locations = nlp.process_answer_location(userText)
            print(job_locations)
            if job_locations == []:
                return "I didn't catch any location, please try again."
            if (job_titles != [] and job_locations != []):
                find_job_offers_async(
                    job_titles=job_titles, job_locations=job_locations)

        if (current_question == "Would you like to start the job search?"):
            if userText is not None and (nlp.is_positive_response(userText.lower())):
                current_step = "start_job_search"
            elif userText is not None and (nlp.is_negative_response(userText.lower())):
                if (last_step != "conversation"):
                    # User wants to engage in a conversation about advice and job-related topics
                    current_step = "conversation"
                    topic = get_random_conversation_topic()
                    return f"Sure! Let's talk about {topic}. What would you like to know or discuss?"
                current_step = "conversation"
            else:
                return "I'm sorry, I didn't understand your response. Could you please answer with 'yes' or 'no' in a different way? For example, you can say 'absolutely' or 'not at the moment'."

        else:
            # save_answer(question, answer)
            if userText is not None:
                answers.append(userText)
            else:
                return "I didn't catch any answer, please try again."
            askedQuestions.append(current_question)
            current_question = get_next_question()
            return current_question

    if current_step == "start_job_search" or (userText is not None and nlp.want_to_start_job_search(userText.lower())):
        # Check if the job search has started or if the user wants to continue with questions
        if userText is not None and userText.lower() == "yes":
            # User wants the bot to start searching on the web
            job_search_started = True
            # Add code to initiate the job search using a web scraper and return fake job offers
            job_offers = get_job_offers()

            df = pd.DataFrame(
                {'Questions': askedQuestions, 'Answers': answers})
            df['Combined_Answers'] = ' '.join(answers)
            find_the_best_job(df, job_offers)

            return "Job search initiated. Here are some job offers for you:\n\n"

    if current_step == "conversation":
        if random.random() < 0.3:
            # Ask if the user wants to start the job search
            last_step = current_step
            current_step = "start"
            return "By the way, would you like the start answering the questions now?"

    # If the code reaches this point, handle any unexpected or unrecognized user input
    return response


# webview.create_window("JOBOT",app)


if __name__ == "__main__":
    app.run(debug=False)
    # webview.start()
