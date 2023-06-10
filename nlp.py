import spacy

import spacy
model_path = "models/en_core_web_sm-3.5.0"
nlp = spacy.load(model_path)

# def process_answer(answer):
#     doc = nlp(answer)

#     # Perform named entity recognition (NER)
#     entities = [(ent.text, ent.label_) for ent in doc.ents]

#     # Perform part-of-speech (POS) tagging
#     pos_tags = [(token.text, token.pos_) for token in doc]

#     # Perform dependency parsing
#     dependencies = [(token.text, token.dep_, token.head.text) for token in doc]

#     # You can add more processing or extraction logic as needed

#     return entities, pos_tags, dependencies


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
