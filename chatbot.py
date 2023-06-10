from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
CB = ChatBot('ChatBot')

# Training with Personal Ques & Ans
trainer = ListTrainer(CB)

# Additional Training Data (continued)
conversation = [
    "hi",
    "Hi there!",
    "Are you looking for a job?",
    "Yes, I am looking for a job.",
    "Great! What are your skills and areas of expertise?",
    "I have experience in programming and web development.",
    "That's fantastic! What is your educational background?",
    "I have a bachelor's degree in computer science.",
    "Perfect! Are you willing to travel or relocate for a job?",
    "Yes, I am open to both travel and relocation.",
    "Excellent! Do you have a preference between working from home, working from the office, or a hybrid mode?",
    "I prefer a hybrid mode with a combination of remote and office work.",
    "Noted. Where do you prefer to work? Which city?",
    "I prefer to work in Tel Aviv, Israel.",
    "Alright. What percentage of the workday will you be expected to work, and what specific hours or days will you be required to work?",
    "I am available for full-time work and can work from 9 AM to 6 PM, Monday to Friday.",
    "Good to know! What type of industry are you interested in?",
    "I am interested in the technology and software development industry.",
    "Great choice! What are your interests and passions?",
    "I am passionate about creating innovative software solutions and staying updated with the latest technologies.",
    "That's wonderful! What type of work-related activities do you enjoy outside of work?",
    "I enjoy attending tech meetups and participating in hackathons.",
    "Impressive! What is your level of experience?",
    "I have 3 years of professional experience in software development.",
    "Awesome! Are there any companies that you are particularly interested in working for?",
    "I am particularly interested in working for tech startups with a strong focus on innovation.",
    "Thank you for providing your information. We will now initiate the job search process. Please wait while we find suitable job options for you.",
    "Sure, take your time. I'll be here if you need any further assistance.",
    "Would you like to start the job search now or continue answering more questions?",
    "I'm ready to start the job search.",
    "Great! We will begin the search and provide you with the best job options based on your preferences.",
    "I would like to answer more questions before starting the job search.",
    "No problem. Let's continue with the questions, and once you're ready, we can initiate the job search.",
    "What is your desired salary range for a job?",
    "I am looking for a salary range of $50,000 to $70,000 per year.",
    "Understood. We will consider this range while searching for suitable job opportunities.",
    "Do you have any specific job titles or positions in mind?",
    "I am specifically interested in software developer or web developer positions.",
    "Noted. We will focus on finding job opportunities in those roles.",
    "Would you like to receive email notifications for new job offers?",
    "Yes, please send me email notifications for new job offers.",
    "Perfect! We will keep you updated with relevant job opportunities via email.",
    "Thank you for answering the questions. We will now proceed with the job search. Please wait while we find suitable job options for you.",
    "Sure, take your time. I'll be here if you need any further assistance.",
    "Would you like to start the job search now or continue answering more questions?",
    "I'm ready to start the job search.",
    "Great! We will begin the search and provide you with the best job options based on your preferences.",
    "I would like to answer more questions before starting the job search.",
    "No problem. Let's continue with the questions, and once you're ready, we can initiate the job search.",
    "What is your desired salary range for a job?",
    "I am looking for a salary range of $50,000 to $70,000 per year.",
    "Understood. We will consider this range while searching for suitable job opportunities.",
    "Do you have any specific job titles or positions in mind?",
    "I am specifically interested in software developer or web developer positions.",
    "Noted. We will focus on finding job opportunities in those roles.",
    "Would you like to receive email notifications for new job offers?",
    "Yes, please send me email notifications for new job offers.",
    "Perfect! We will keep you updated with relevant job opportunities via email.",
    "Thank you for answering the questions. We will now proceed with the job search. Please wait while we find suitable job options for you.",
    "Sure, take your time. I'll be here if you need any further assistance.",
    "Would you like to start the job search now or continue answering more questions?",
    "I'm ready to start the job search.",
    "Great! We will begin the search and provide you with the best job options based on your preferences.",
    "I would like to answer more questions before starting the job search.",
    "No problem. Let's continue with the questions, and once you're ready, we can initiate the job search.",
    "Is there any specific location you prefer for the job?",
    "Yes, I prefer jobs in the San Francisco Bay Area.",
    "Noted. We will focus on finding job opportunities in the San Francisco Bay Area.",
    "Do you have any particular company in mind where you would like to work?",
    "Yes, I would love to work for Google if possible.",
    "Great choice! We will consider Google as one of the target companies while searching for job opportunities.",
    "Thank you for providing your information. We will now initiate the job search process. Please wait while we find suitable job options for you.",
    "Sure, take your time. I'll be here if you need any further assistance.",
    "Would you like to start the job search now or continue answering more questions?",
    "I'm ready to start the job search.",
    "Great! We will begin the search and provide you with the best job options based on your preferences.",
    "I would like to answer more questions before starting the job search.",
    "No problem. Let's continue with the questions, and once you're ready, we can initiate the job search."
]

# Training the ChatBot with Additional Data
trainer.train(conversation)

conversation = [
    "Hello!",
    "Hi there! Are you currently looking for a job?",
    "Yes, I am. Can you help me with job search?",
    "Absolutely! I'll ask you a few questions to understand your preferences and then search for suitable job options. Let's get started!",
    "What are your skills and areas of expertise? (e.g. programming, design, marketing)",
    "I have skills in programming and web development.",
    "Great! What is your educational background? (degrees, certifications)",
    "I have a Bachelor's degree in Computer Science and a certification in Full Stack Web Development.",
    "Are you willing to travel or relocate for a job?",
    "I am open to both travel and relocation for the right job opportunity.",
    "Do you have a preference between working from home, working from the office, or a hybrid mode?",
    "I prefer a hybrid mode where I can work partly from home and partly from the office.",
    "What location are you looking to work in?",
    "I am interested in job opportunities in New York City.",
    "What type of employment are you seeking? Full-time, part-time, contract?",
    "I am looking for full-time employment.",
    "What is your desired salary range?",
    "I am aiming for a salary range of $60,000 to $80,000 per year.",
    "Thank you for answering the questions. Based on your responses, I will search for job opportunities that match your preferences. Please wait while I generate the results.",
    "Sure, take your time. Let me know if you need any further information.",
    "I have found some suitable job options for you. Here are the links:",
    "Thank you! I will check out the job options and apply accordingly.",
    "You're welcome! If you have any more questions or need assistance, feel free to ask."
]

trainer.train(conversation)
 
conversation = [
    "Hello!",
    "Hi there! Are you currently looking for a job?",
    "Yes, I am. Can you help me with job search?",
    "Absolutely! I'll ask you a few questions to understand your preferences and then search for suitable job options. Let's get started!",
    "What are your skills and areas of expertise? (e.g. programming, design, marketing)",
    "I have skills in programming and web development.",
    "Great! What is your educational background? (degrees, certifications)",
    "I have a Bachelor's degree in Computer Science and a certification in Full Stack Web Development.",
    "Are you willing to travel or relocate for a job?",
    "I am open to both travel and relocation for the right job opportunity.",
    "Do you have a preference between working from home, working from the office, or a hybrid mode?",
    "I prefer a hybrid mode where I can work partly from home and partly from the office.",
    "What location are you looking to work in?",
    "I am interested in job opportunities in New York City.",
    "What type of employment are you seeking? Full-time, part-time, contract?",
    "I am looking for full-time employment.",
    "What is your desired salary range?",
    "I am aiming for a salary range of $60,000 to $80,000 per year.",
    "Thank you for answering the questions. Based on your responses, I will search for job opportunities that match your preferences. Please wait while I generate the results.",
    "Sure, take your time. Let me know if you need any further information.",
    "I have found some suitable job options for you. Here are the links:",
    "Thank you! I will check out the job options and apply accordingly.",
    "You're welcome! If you have any more questions or need assistance, feel free to ask."
]

# Training the ChatBot with Additional Data
trainer.train(conversation)

# Training with English Corpus Data
#trainer_corpus = ChatterBotCorpusTrainer(CB)
#trainer_corpus.train('chatterbot.corpus.english')
