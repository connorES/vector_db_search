from utils.constants import DESC_KEYWORD_BONUS, TITLE_KEYWORD_BONUS
from utils.tech_keyword_list import tech_keyword_list
import re
from classes.job import Job
from classes.candidate import Candidate


def add_bonus_score(input, results):
    
    def process_result(result, title_keywords, desc_keywords, tech_keywords):
        bonus = get_bonus_score(title_keywords, desc_keywords, tech_keywords)
        final_score = result.score + bonus
        return (result, final_score)

    def get_keywords_for_candidate(result):
        return (
            find_langs(result.payload['title']),
            result.payload['tech_keywords'],
            input.tech_keywords
        )

    def get_keywords_for_job(result):
        return (
            input.title_tech_keywords,
            input.desc_tech_keywords,
            result.payload['tech_keywords']
        )

    def get_keywords_for_string(result):
        return (
            [],
            desc_keywords,
            result.payload['tech_keywords']
        )

    if isinstance(input, Candidate):
        get_keywords = get_keywords_for_candidate
    elif isinstance(input, Job):
        get_keywords = get_keywords_for_job
    elif isinstance(input, str):
        desc_keywords = find_langs(input)
        get_keywords = get_keywords_for_string
    else:
        raise ValueError("Invalid input object type")

    scored_results = [
        process_result(result, *get_keywords(result))
        for result in results
    ]

    return sorted(scored_results, key=lambda x: x[1], reverse=True)


# This function checks a resume for keywords and then retruns the score to be added
def check_resume(desc_tech_keywords: list, title_tech_keywords: list, resume_tech_keywords: list):
    if not resume_tech_keywords:
        return 0

    def get_multiplier(keywords):
        try:
            num = len(
                [word for word in keywords if word in resume_tech_keywords]) / len(keywords)
            return num
        except ZeroDivisionError:
            return 0

    desc_multiplier = get_multiplier(desc_tech_keywords)
    title_multiplier = get_multiplier(title_tech_keywords)

    added_score = (title_multiplier * TITLE_KEYWORD_BONUS) + \
        (desc_multiplier * DESC_KEYWORD_BONUS)
    result = round(added_score, 5)
    return result


def get_bonus_score(job_title_keywords, job_desc_keywords, resume_tech_keywords):
    bonus_score = 0
    bonus_score += check_resume(job_desc_keywords, job_title_keywords,
                                resume_tech_keywords)
    result = round(bonus_score, 5)
    return result


def clean_string(input_string):
    # Define a regular expression pattern to match symbols, punctuation, and unusual characters
    pattern = r'[^a-zA-Z0-9\s+#]'
    # Replace the matched characters with a space
    cleaned_string = re.sub(pattern, ' ', input_string)
    return cleaned_string


def generate_ngrams(input_words: list, n: int) -> list:
    # Generate n-grams from the list of words
    ngrams = [' '.join(input_words[i:i+n])
              for i in range(len(input_words)-n+1)]
    return ngrams


def find_langs(input_string: str):
    # Clean and split the input string into words
    cleaned_string = clean_string(input_string).lower()
    input_words = cleaned_string.split()
    bi_grams = generate_ngrams(input_words, 2)

    # Initialize a set to store found keywords
    found_keywords = []
    for word in tech_keyword_list:
        word = word.lower()
        if " " in word:
            if word in bi_grams:
                found_keywords.append(word)
                continue
        if word in input_words:
            found_keywords.append(word)

    return list(found_keywords)
