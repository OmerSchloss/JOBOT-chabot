import spacy
import re

model_path = "models/en_core_web_sm-3.5.0"
nlp = spacy.load(model_path)  # type: ignore

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

    positive_keywords = ['yes', 'yeah', 'absolutely',
                         'definitely', 'certainly', 'sure', 'of course']

    for token in doc:
        if token.lemma_ in positive_keywords:
            return True

    return False


def is_negative_response(text):
    doc = nlp(text)

    negative_keywords = ['no', 'nope', 'not really',
                         'not interested', 'don\'t', 'do not', 'never']

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


def process_answer_job_title(text):
    # Process the job title answer
    doc_job_title = nlp(text)
    relevant_job_titles = []

    # Check for noun phrases consisting of consecutive nouns
    i = 0
    while i < len(doc_job_title):
        if doc_job_title[i].pos_ == 'NOUN':
            j = i + 1
            while j < len(doc_job_title) and doc_job_title[j].pos_ == 'NOUN':
                j += 1
            if j > i + 1:
                job_title = ' '.join(
                    [token.text for token in doc_job_title[i:j]])
                if job_title not in relevant_job_titles:
                    relevant_job_titles.append(job_title)
            else:
                # Append the individual noun as a separate job title if not already in the list
                if doc_job_title[i].text not in relevant_job_titles:
                    relevant_job_titles.append(doc_job_title[i].text)
            i = j
        else:
            i += 1

    # Check for single-word job titles and add them only if not already in any multi-word job title
    for token in doc_job_title:
        if token.pos_ == 'NOUN':
            is_single_word_title = True
            for title in relevant_job_titles:
                if token.text in title.split():
                    is_single_word_title = False
                    break
            if is_single_word_title:
                relevant_job_titles.append(token.text)

    return relevant_job_titles


def process_answer_location(text):
    relevant_locations = []

    cities_in_israel = [
        'jerusalem',
        'tel aviv',
        'haifa',
        'rishon lezion',
        'petah tikva',
        'ashdod',
        'netanya',
        'beer sheva',
        'bnei brak',
        'holon',
        'ramat gan',
        'bat yam',
        'ashkelon',
        'herzliya',
        'kfar saba',
        'ra\'anana',
        'modi\'in-maccabim-re\'ut',
        'nahariya',
        'lod',
        'ramla',
        'beit shemesh',
        'rehovot',
        'jaffa',
        'eilat',
        'acre',
        'nazareth',
        'kiryat gat',
        'kiryat motzkin',
        'hadera',
        'ma\'alot-tarshiha',
        'yavne',
        'tiberias',
        'dimona',
        'ofakim',
        'sderot',
        'yehud',
        'orma',
        'tirat carmel',
        'arraba',
        'karmiel',
        'givatayim',
        'eilabun',
        'kiryat bialik',
        'sakhnin',
        'arad',
        'modi\'in illit',
        'tayibe',
        'rahat',
        'nablus',
        'qalqilyah',
        'hebron',
        'bethlehem',
        'ramallah',
        'gaza',
        'beit lahia',
        'nur shams',
        'deir al-balah',
        'tulkarm',
        'qalansawe',
        'um al-fahm',
        'haifa bay',
        'west jerusalem',
        'east jerusalem',
        'tel aviv yafo',
        'tel aviv district',
        'central district',
        'southern district',
        'northern district',
        'haifa district',
        'jerusalem district',
        'rishon lezion district',
        'petah tikva district',
        'ashdod district',
        'netanya district',
        'beer sheva district',
        'bnei brak district',
        'holon district',
        'ramat gan district',
        'bat yam district',
        'ashkelon district',
        'herzliya district',
        'kfar saba district',
        'ra\'anana district',
        'nahariya district',
        'lod district',
        'ramla district',
        'beit shemesh district',
        'rehovot district',
        'jaffa district',
        'eilat district',
        'acre district',
        'nazareth district',
        'kiryat gat district',
        'kiryat motzkin district',
        'hadera district',
        'ma\'alot-tarshiha district',
        'yavne district',
        'tiberias district',
        'dimona district',
        'ofakim district',
        'sderot district',
        'yehud district',
        'orma district',
        'tirat carmel district',
        'arraba district',
        'karmiel district',
        'givatayim district',
        'eilabun district',
        'kiryat bialik district',
        'sakhnin district',
        'arad district',
        'modi\'in illit district',
        'tayibe district',
        'rahat district',
        'nablus district',
        'qalqilyah district',
        'hebron district',
        'bethlehem district',
        'ramallah district',
        'gaza district',
        'beit lahia district',
        'nur shams district',
        'deir al-balah district',
        'tulkarm district',
        'qalansawe district',
        'um al-fahm district',
        'haifa bay district',
        'west jerusalem district',
        'east jerusalem district',
        'tel aviv yafo district'
        # Add more cities or districts as needed
    ]

    doc_location = nlp(text)

    for ent in doc_location.ents:
        if ent.label_ == 'GPE' or ent.text.lower() in [city.lower() for city in cities_in_israel]:
            relevant_locations.append(ent.text)

    for city in cities_in_israel:
        if city.lower() in text.lower() and city not in relevant_locations:
            relevant_locations.append(city)

    return relevant_locations


def process_answer_job_type(text):
    doc = nlp(text)
    job_type = ''

    keyword_synonyms = {
        "permanent": ["permanent", "full-time", "regular", "ongoing", "stable", "long-term", "career", "salaried", "professional", "standard", "secure", "stable", "steadfast", "consistent"],
        "fulltime": ["fulltime", "full-time", "standard", "fixed", "traditional", "conventional", "usual", "normal"],
        "temporary": ["temporary", "temp", "short-term", "seasonal", "part-time", "contractual", "hourly", "flexible", "interim", "occasional", "freelance", "project-based"],
        "internship": ["internship", "intern", "traineeship", "apprenticeship", "learning", "development", "educational", "practical"],
        "contract": ["contract", "freelance", "project-based", "temporary", "hourly", "consulting", "self-employed", "gig", "independent", "outsourced", "non-permanent"]
    }

    for token in doc:
        for j_type, synonyms in keyword_synonyms.items():
            if token.text.lower() in synonyms:
                job_type = j_type
                break
        if job_type:
            break

    return job_type


def get_short_description(text):
    doc = nlp(text)

    # Extract sentences from the parsed document
    sentences = [sent.text for sent in doc.sents]

    # Select the first few sentences as the short description
    num_sentences = 3  # Define the number of sentences for the short description
    short_description = ' '.join(sentences[:num_sentences])

    return short_description
