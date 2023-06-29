import random
import spacy

model_path = "models/en_core_web_sm-3.5.0"
nlp = spacy.load(model_path)

conversation_topics = [
    "resume",
    "networking",
    "interview preparation",
    "career development",
    "work-life balance"
]

tips_by_topic = {
    "resume": [
        "Tailor your resume to highlight relevant skills and experiences.",
        "Use action verbs to describe your achievements and responsibilities.",
        "Keep your resume concise and easy to read.",
        "Include keywords related to the job position you're applying for.",
        "Proofread your resume to ensure there are no typos or errors."
    ],
    "networking": [
        "Attend industry events and conferences to expand your professional network.",
        "Connect with professionals on LinkedIn and engage in meaningful conversations.",
        "Join relevant professional groups and associations.",
        "Follow up with contacts after networking events to maintain connections.",
        "Offer assistance and support to others in your network."
    ],
    "interview preparation": [
        "Research the company and the position you're applying for.",
        "Practice answering common interview questions.",
        "Prepare examples of your achievements and experiences.",
        "Dress professionally and arrive on time for the interview.",
        "Ask thoughtful questions to demonstrate your interest."
    ],
    "career development": [
        "Set clear goals and create a plan for your career growth.",
        "Continuously update your skills through training and education.",
        "Seek mentorship and guidance from experienced professionals.",
        "Take on new challenges and responsibilities to expand your expertise.",
        "Regularly assess and evaluate your career progress."
    ],
    "work-life balance": [
        "Establish boundaries between work and personal life.",
        "Prioritize self-care activities such as exercise, relaxation, and hobbies.",
        "Delegate tasks and learn to say no when necessary.",
        "Create a schedule that allows for both work and personal time.",
        "Communicate your needs and expectations with your employer and colleagues."
    ]
}

advice_by_topic = {
    "resume": [
        "Seek feedback from professionals or resume experts to improve your resume.",
        "Customize your resume for each job application to make it more impactful.",
        "Highlight your key accomplishments and achievements in each work experience section.",
        "Include relevant certifications or training courses to showcase your skills.",
        "Consider using a professional resume template for a polished look."
    ],
    "networking": [
        "Attend networking events with a specific goal or objective in mind.",
        "Follow up with a personalized thank-you note after meeting someone new.",
        "Leverage online networking platforms to connect with professionals in your field.",
        "Offer to help others in your network by sharing valuable resources or insights.",
        "Build and maintain genuine relationships by staying in touch with your connections."
    ],
    "interview preparation": [
        "Research common interview questions and practice your responses.",
        "Prepare insightful questions to ask the interviewer about the company or role.",
        "Utilize mock interviews or role-playing exercises to enhance your interview skills.",
        "Focus on showcasing your relevant skills and experiences during the interview.",
        "Demonstrate your enthusiasm and passion for the opportunity during the interview."
    ],
    "career development": [
        "Seek opportunities to take on leadership roles or lead projects within your organization.",
        "Invest in professional development courses or certifications to enhance your skills.",
        "Build a strong personal brand online through blogging or social media engagement.",
        "Network with professionals in your desired career field to gain insights and guidance.",
        "Regularly reassess your career goals and make adjustments as needed."
    ],
    "work-life balance": [
        "Practice effective time management techniques to prioritize your tasks and responsibilities.",
        "Establish a dedicated workspace at home to create separation between work and personal life.",
        "Take regular breaks and engage in activities that help you relax and recharge.",
        "Consider flexible work arrangements or discussing work-life balance with your employer.",
        "Seek support from friends, family, or mentors to maintain a healthy work-life balance."
    ]
}


def get_random_conversation_topic():
    # Retrieve a random conversation topic
    return random.choice(conversation_topics)


def generate_conversation_response(topic, user_input):
    if topic.lower() not in conversation_topics:
        return "I'm sorry, but I'm not knowledgeable about that topic at the moment."

    doc = nlp(user_input.lower())
    if any(token.text in ("tips", "tip") for token in doc):
        topic_tips = tips_by_topic.get(topic.lower())
        if topic_tips:
            response = random.choice(topic_tips)
            topic_tips.remove(response)
            return response + "<br>If you want more tips on this topic, just let me know!"
        else:
            return "I'm sorry, but I don't have any tips on that topic at the moment."

    if any(token.text in ("advice", "advices") for token in doc):
        topic_advice = advice_by_topic.get(topic.lower())
        if topic_advice:
            response = random.choice(topic_advice)
            topic_advice.remove(response)
            return response + "<br>If you want more advice on this topic, just let me know!"
        else:
            return "I'm sorry, but I don't have any advice on that topic at the moment."

    return "Sure! I can provide tips and advice on " + topic.lower() + ". Just let me know if you want tips or advice."
