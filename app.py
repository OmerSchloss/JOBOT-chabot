import random
# from chatbot import CB
from flask import Flask, render_template, request

import nlp
# import webview

# app = Flask(__name__)
app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Conversation flow questions
questions = [
    "What are your skills and areas of expertise?",
    "What is your educational background?",
    "Are you willing to travel or relocate for a job?",
    "What type of job are you looking for? Full-time? Part-time?",
    "Do you have a preference between working from home, working from the office, or a hybrid mode?",
    "Where do you prefer to work? Which city?",
    "What percentage of the workday will you be expected to work, and what specific hours or days will you be required to work?",
    "What type of industry are you interested in?",
    "What are your interests and passions?",
    "What type of work-related activities do you enjoy outside of work?",
    "What is your level of experience?",
    "Are there any companies that you are particularly interested in working for?",
    "Would you like to start the job search?"
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


def get_next_question():
    # Retrieve the next question based on the conversation flow
    # If there are no more questions, return "start job search"
    if len(questions) > 0:
        return questions.pop(0)
    else:
        return "start job search"


def get_random_conversation_topic():
    # Retrieve a random conversation topic
    return random.choice(conversation_topics)


@app.route("/chatbot")
def home():
    return render_template("index.html")


@app.route("/reset")
def reset_conversation():

    questions = [
        "What are your skills and areas of expertise?",
        "What is your educational background?",
        "Are you willing to travel or relocate for a job?",
        "What type of job are you looking for? Full-time? Part-time?",
        "Do you have a preference between working from home, working from the office, or a hybrid mode?",
        "Where do you prefer to work? Which city?",
        "What percentage of the workday will you be expected to work, and what specific hours or days will you be required to work?",
        "What type of industry are you interested in?",
        "What are your interests and passions?",
        "What type of work-related activities do you enjoy outside of work?",
        "What is your level of experience?",
        "Are there any companies that you are particularly interested in working for?",
        "Would you like to start the job search?"
    ]

    global last_step
    global current_step
    global current_question
    global job_search_started
    global answers

    answers = []
    last_step = None
    current_step = None
    current_question = None
    job_search_started = False

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
        # Store user's answer in the database
        question = current_question
        answer = userText
        # save_answer(question, answer)
        # processed_answer = nlp.process_answer(answer)
        answers.append((question, answer))

        if (question == "Would you like to start the job search?"):
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
            current_question = get_next_question()
            return current_question

    if current_step == "start_job_search" or (userText is not None and nlp.want_to_start_job_search(userText.lower())):
        # Check if the job search has started or if the user wants to continue with questions
        if userText is not None and userText.lower() == "yes":
            # User wants the bot to start searching on the web
            job_search_started = True
            # Add code to initiate the job search using a web scraper and return fake job offers
            job_offers = generate_fake_job_offers()
            return "Job search initiated. Here are some job offers for you:\n\n" + "\n".join(job_offers)

    if current_step == "conversation":
        if random.random() < 0.3:
            # Ask if the user wants to start the job search
            last_step = current_step
            current_step = "start"
            return "By the way, would you like the start answering the questions now?"

    # If the code reaches this point, handle any unexpected or unrecognized user input
    return response


def generate_fake_job_offers():
    # Add code to generate fake job offers using a web scraper or predefined data
    job_offers = ["Software Engineer at ABC Company",
                  "Marketing Specialist at XYZ Corporation",
                  "Data Analyst at DEF Industries",
                  "Project Manager at GHI Solutions",
                  "Graphic Designer at JKL Agency"]
    return job_offers

# webview.create_window("JOBOT",app)


if __name__ == "__main__":
    app.run(debug=False)
    # webview.start()
