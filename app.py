import random
import json
from flask import Flask, render_template, request
import pandas as pd
from FindBestJob import find_the_best_job
from jobScraper import find_all_job_offers, get_all_job_offers
import nlp


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
    "job_link": "",
    "job_offers": [],
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
        "job_link": "",
        "job_offers": [],
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

    if state["current_step"] != 'job_offers_step' and state["job_search_started"] == False and state["job_titles"] != [] and state["job_locations"] != [] and state["job_type"] != "":
        state["job_search_started"] = True
        find_all_job_offers(
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
                    find_all_job_offers(
                        job_titles=state["job_titles"], job_locations=state["job_locations"], job_type=state["job_type"])
            else:
                return "I didn't catch any job type, would you like to try again?."

        if (state["current_question"] == "Would you like to start the job search?"):
            if userText is not None and (nlp.is_positive_response(userText.lower())):
                state["current_step"] = "job_search_step"
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

    if state["current_step"] == "job_search_step" or (userText is not None and nlp.want_to_start_job_search(userText.lower())):
        # Check if the job search has started or if the user wants to continue with questions
        if userText is not None and nlp.is_positive_response(userText.lower()):
            if state["job_search_started"] == False:
                state["job_search_started"] = True
                find_all_job_offers(
                    job_titles=state["job_titles"], job_locations=state["job_locations"], job_type=state["job_type"])

            state["job_offers"] = get_all_job_offers()

            df = pd.DataFrame(
                {'Questions': state["askedQuestions"], 'Answers': state["answers"]})
            df['Combined_Answers'] = ' '.join(state["answers"])
            new_offer, state["job_link"], state["job_key"] = find_the_best_job(
                df, state["job_offers"])
            new_job_offer = "I have found for you {} suitable job offers!<br>I think this one will be the best suited for you:<br><br>{}".format(
                len(state["job_offers"]), new_offer)

            state["job_offers"] = [obj for obj in state["job_offers"]
                                   if obj['job_key'] != state["job_key"]]
            state["current_question"] = 'Would you like to see more about this job and apply?'
            state["current_step"] = 'job_offers_step'
            # Save the state
            save_state()
            return "{}<br><br>{}".format(new_job_offer, state["current_question"])

    if state["current_step"] == 'job_offers_step':
        if (state["current_question"] == 'Would you like to see more about this job and apply?'):
            if userText is not None and (nlp.is_positive_response(userText.lower())):
                state["current_question"] = 'Would you like to get another job offer that might be suited for you?'
                # Save the state
                save_state()
                return 'Here is the link:<br> {} <br>{}'.format(state["job_link"], state["current_question"])
            elif userText is not None and (nlp.is_negative_response(userText.lower())):
                state["current_question"] = 'Would you like to get another job offer that might be suited for you?'
                # Save the state
                save_state()
                return state["current_question"]
            else:
                return "I'm sorry, I didn't understand your response."
        if (state["current_question"] == 'Would you like to get another job offer that might be suited for you?'):
            df = pd.DataFrame(
                {'Questions': state["askedQuestions"], 'Answers': state["answers"]})
            df['Combined_Answers'] = ' '.join(state["answers"])
            new_offer, state["job_link"], state["job_key"] = find_the_best_job(
                df, state["job_offers"])
            
            state["job_offers"] = [obj for obj in state["job_offers"]
                                   if obj['job_key'] != state["job_key"]]
            new_job_offer = "I have found for you {} suitable job offers!<br>here is a new job offer:<br><br>{}".format(
                len(state["job_offers"]), new_offer)
            state["current_question"] = 'Would you like to see more about this job and apply?'
            # Save the state
            save_state()
            return "{}<br><br>{}".format(new_job_offer, state["current_question"])

    if state["current_step"] == "conversation":
        if random.random() < 0.3:
            # Ask if the user wants to start the job search
            state["last_step"] = state["current_step"]
            state["current_step"] = "start"
            return "By the way, would you like the start answering the questions now?"

    # If the code reaches this point, handle any unexpected or unrecognized user input
    return response


if __name__ == "__main__" or __name__ == "app":
    # Restore the state
    restore_state()

    # app.run(debug=False, port=7085)
    app.run(host="0.0.0.0", port=7085)
