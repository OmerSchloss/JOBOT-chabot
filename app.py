import random
import json
from flask import Flask, render_template, request
import pandas as pd
from FindBestJob import find_the_best_job
import nlp

from jobScraper_Google import find_job_offers_async_in_Google, get_job_offers_in_Google
from jobScraper_Indeed import find_job_offers_async_in_Indeed, get_job_offers_in_Indeed
from jobScraper_JobIsJob import find_job_offers_async_in_JobIsJob, get_job_offers_in_JobIsJob
from jobScraper_LinkUp import find_job_offers_async_in_LinkUp, get_job_offers_in_LinkUp
from jobscraper_Monster import find_job_offers_async_in_Monster, get_job_offers_in_Monster
from jobScraper_SimplyHired import find_job_offers_async_in_SimplyHired, get_job_offers_in_SimplyHired
from jobScraper_SnagaJob import find_job_offers_async_in_SnagaJob, get_job_offers_in_SnagaJob

app = Flask(__name__, template_folder='./templates', static_folder='./static')

conversation_topics = [
    "resume",
    "networking",
    "interview preparation",
    "career development",
    "work-life balance"
]

state = {
    "last_step": None,
    "current_step": None,
    "current_question": None,
    "job_search_started": False,
    "questions": [
        "What is your preferred job title or role?",
        "What is your preferred location for the job?",
        "Are you looking for full-time, part-time, internship, or contract opportunities?",
        "What industry or field are you interested in?",
        "How many years of experience do you have in this field?",
        "What are your specific skills or areas of expertise?",
        "Are you open to remote work or do you prefer on-site positions?",
        "What is your desired salary range?",
        "Are there any specific companies or organizations you would like to work for?",
        "What level of education or certifications do you possess?",
        "Are there any specific job benefits or perks you value?"
    ],
    "answers": [],
    "askedQuestions": [],
    "job_titles": None,
    "job_locations": None,
    "job_type": "",
    "isRestored": ""
}

# Path to the state file
state_file_path = "state.txt"


def save_state():
    # Save the state to the state file
    with open(state_file_path, "w") as file:
        json.dump(state, file)


def restore_state():
    print("restore...")
    global state
    # Restore the state from the state file if it exists
    try:
        with open(state_file_path, "r") as file:
            state.update(json.load(file))
        print("restored!")
        state['isRestored'] = True
    except FileNotFoundError:
        pass


def get_next_question():
    # Retrieve the next question based on the conversation flow
    # If there are no more questions, return "start job search"
    if len(state["questions"]) > 0:
        return state["questions"].pop(0)
    else:
        return "Would you like to start the job search?"


def get_random_conversation_topic():
    # Retrieve a random conversation topic
    return random.choice(conversation_topics)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reset")
def reset_conversation():
    global state

    # Reset the state
    state = {
        "last_step": None,
        "current_step": None,
        "current_question": None,
        "job_search_started": False,
        "questions": [
            "What is your preferred job title or role?",
            "What is your preferred location for the job?",
            "Are you looking for full-time, part-time, internship, or contract opportunities?",
            "What industry or field are you interested in?",
            "How many years of experience do you have in this field?",
            "What are your specific skills or areas of expertise?",
            "Are you open to remote work or do you prefer on-site positions?",
            "What is your desired salary range?",
            "Are there any specific companies or organizations you would like to work for?",
            "What level of education or certifications do you possess?",
            "Are there any specific job benefits or perks you value?"
        ],
        "answers": [],
        "askedQuestions": [],
        "job_titles": [],
        "job_locations": [],
        "job_type": "",
        "isRestored": False
    }

    # Save the state
    save_state()

    return "Conversation has been reset. You can now start a new conversation."


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = 'well'  # str(CB.get_response(userText))

    global state

    if (state['isRestored']):
        state["job_search_started"] = False
        state['isRestored'] = False

    if state["job_search_started"] == False and state["job_titles"] != [] and state["job_locations"] == [] and state["job_type"] != "":
        state["job_search_started"] = True
        find_job_offers_async_in_Indeed(
            job_titles=state["job_titles"], job_locations=state["job_locations"], job_type=state["job_type"])

    if state["current_step"] is None:
        # Welcome message and first question to start the conversation
        welcome_message = "Hello! I'm here to assist you with your job search. Would you like to start?"
        state["current_step"] = "start"
        # Save the state
        save_state()
        return welcome_message

    if state["current_step"] == "start":
        if userText is not None and (nlp.is_positive_response(userText.lower())):
            # User wants to start the job search
            state["current_step"] = "questions"
            state["current_question"] = get_next_question()
            # Save the state
            save_state()
            return state["current_question"]
        elif userText is not None and (nlp.is_negative_response(userText.lower())):
            if (state["last_step"] != "conversation"):
                # User wants to engage in a conversation about advice and job-related topics
                state["current_step"] = "conversation"
                topic = get_random_conversation_topic()
                return f"Sure! Let's talk about {topic}. What would you like to know or discuss?"
            state["current_step"] = "conversation"
        else:
            return "I'm sorry, I didn't understand your response. Could you please answer with 'yes' or 'no' in a different way? For example, you can say 'absolutely' or 'not at the moment'."

    if state["current_step"] == "questions":
        if state["current_question"] == "What is your preferred job title or role?":
            state["job_titles"] = nlp.process_answer_job_title(userText)
            print(state["job_titles"])
            if state["job_titles"] == []:
                return "I didn't catch any job title, please try again."

        if state["current_question"] == "What is your preferred location for the job?":
            state["job_locations"] = nlp.process_answer_location(userText)
            print(state["job_locations"])
            if state["job_locations"] == []:
                return "I didn't catch any location, please try again."

        if state["current_question"] == "Are you looking for full-time, part-time, internship, or contract opportunities?":
            state["job_type"] = nlp.process_answer_job_type(userText)
            print(state["job_type"])

            if (nlp.is_negative_response(userText) or state["job_type"] != ''):
                if state["job_type"] == '':
                    state["job_type"] = 'not_relevant'
                if (state["job_search_started"] == False):
                    state["job_search_started"] = True
                    find_job_offers_async_in_Indeed(
                        job_titles=state["job_titles"], job_locations=state["job_locations"], job_type=state["job_type"])
            else:
                return "I didn't catch any job type, would you like to try again?."

        if (state["current_question"] == "Would you like to start the job search?"):
            if userText is not None and (nlp.is_positive_response(userText.lower())):
                state["current_step"] = "start_job_search"
            elif userText is not None and (nlp.is_negative_response(userText.lower())):
                if (state["last_step"] != "conversation"):
                    # User wants to engage in a conversation about advice and job-related topics
                    state["current_step"] = "conversation"
                    topic = get_random_conversation_topic()
                    return f"Sure! Let's talk about {topic}. What would you like to know or discuss?"
                state["current_step"] = "conversation"
            else:
                return "I'm sorry, I didn't understand your response. Could you please answer with 'yes' or 'no' in a different way? For example, you can say 'absolutely' or 'not at the moment'."

        else:
            # save_answer(question, answer)
            if userText is not None:
                state["answers"] .append(userText)
            else:
                return "I didn't catch any answer, please try again."
            state["askedQuestions"].append(state["current_question"])
            state["current_question"] = get_next_question()
            # Save the state
            save_state()
            return state["current_question"]

    if state["current_step"] == "start_job_search" or (userText is not None and nlp.want_to_start_job_search(userText.lower())):
        # Check if the job search has started or if the user wants to continue with questions
        if userText is not None and userText.lower() == "yes":
            # User wants the bot to start searching on the web
            # Add code to initiate the job search using a web scraper and return fake job offers
            job_offers = get_job_offers_in_Indeed()

            df = pd.DataFrame(
                {'Questions': state["askedQuestions"], 'Answers': state["answers"]})
            df['Combined_Answers'] = ' '.join(state["answers"])
            new_offer = find_the_best_job(df, job_offers)
            result_string = "I have found for you {} offers!\nHere is the best one:<br><br>{}".format(
                len(job_offers), new_offer)

            return result_string

    if state["current_step"] == "conversation":
        if random.random() < 0.3:
            # Ask if the user wants to start the job search
            state["last_step"] = state["current_step"]
            state["current_step"] = "start"
            return "By the way, would you like the start answering the questions now?"

    # If the code reaches this point, handle any unexpected or unrecognized user input
    return response


if __name__ == "__main__" or __name__ =='app':
    # Restore the state
    restore_state()

    # app.run(debug=False, port=5555)
    app.run(host="0.0.0.0", port=5555)