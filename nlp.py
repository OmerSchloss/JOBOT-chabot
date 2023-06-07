import spacy

# Load spaCy NLP model
nlp = spacy.load('en_core_web_sm')



def is_positive_response(text):
    doc = nlp(text)

    positive_keywords = ['yes', 'yeah', 'absolutely', 'definitely', 'certainly', 'sure', 'of course']

    for token in doc:
        if token.lemma_ in positive_keywords:
            return True

    return False


def is_negative_response(text):
    doc = nlp(text)

    negative_keywords = ['no', 'nope', 'not really', 'not interested', 'don\'t', 'do not', 'never']

    for token in doc:
        if token.lemma_ in negative_keywords:
            return True

    return False

def want_to_start_job_search(text):
    doc = nlp(text)

    start_job_search_keywords = ['start', 'search']

    for token in doc:
        if token.lemma_ in start_job_search_keywords:
            return True

    return False
