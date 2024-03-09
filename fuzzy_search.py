import numpy as np
import nltk
from nltk.stem import PorterStemmer
import joblib
import json
from fuzzywuzzy import fuzz


def fuzzy_search(query, scraped_data):
    matches = []
    if len(query) < 3:
        return matches
    for i, job_data in enumerate(scraped_data):
        title_score = fuzz.partial_ratio(query, job_data["title"])
        description_score = fuzz.partial_ratio(query, job_data["description"])
        
        second_title_score = fuzz.token_sort_ratio(query, job_data["title"])
        second_description_score = fuzz.token_sort_ratio(query, job_data["description"])

        if second_title_score > title_score:
            title_score = second_title_score
        if second_description_score > description_score:
            description_score = second_description_score

        total_score = title_score + description_score

        if title_score > 70 or description_score > 70:
            matches.append((job_data["title"], job_data["link"], job_data["description"], total_score))

    if len(matches) > 0:
        matches = sorted(matches, key=lambda x: x[2], reverse=True)
        matches = [(title, link, description) for title, link, description, _ in matches]

    return matches