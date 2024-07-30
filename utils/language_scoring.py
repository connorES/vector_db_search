from re import sub
from utils.constants import DESC_KEYWORD_BONUS, TITLE_KEYWORD_BONUS, SECURITY_CLEARANCES
from utils.tech_keyword_list import tech_keyword_list


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
    # Log the found keywords

    return list(found_keywords)


def clean_string(input_string):
    # Define a regular expression pattern to match symbols, punctuation, and unusual characters
    pattern = r'[^a-zA-Z0-9\s+#]'
    # Replace the matched characters with a space
    cleaned_string = sub(pattern, ' ', input_string)
    return cleaned_string


def clean_job_title(title):
    # Define pattern to match text within brackets
    pattern = r'\([^()]*\)'
    # Remove text within brackets
    clean_title = sub(pattern, '', title)
    # Remove final 's' if it exists
    if clean_title.endswith('s'):
        clean_title = clean_title[:-1]
    # take out any "X 8" or "8 x"
    clean_title = sub(r'\b\d+\s*[xX]\b|\b[xX]\s*\d+\b', '', clean_title)
    # Replace backslash with space
    clean_title = clean_title.replace('/', ' ')
    # Remove everything after the '-' character
    clean_title = sub(r'-.*', '', clean_title)
    return clean_title


# returns False if the candidate holds an insufficient clearance
def check_clearance(candidate_clearance, job_clearance):

    if not candidate_clearance or not job_clearance:
        return True

    index = SECURITY_CLEARANCES.index(job_clearance)

    if candidate_clearance in SECURITY_CLEARANCES[index:]:
        return True

    return False


def check_location(job, cand):
    if not job.location or not cand.location:
        return True
    if cand.location in job.location:
        return True
    return False


def remove_candidates(job):
    # first remove based on clearance
    to_remove = []
    for cand in job.candidates:
        cand.set_location()
        if not check_clearance(cand, job.clearance):
            to_remove.append(cand)
        if check_location(job, cand) == 0:
            to_remove.append(cand)
    return to_remove


# This function checks a resume for keywords and then retruns the score to be added
def check_resume(desc_tech_keywords: list, title_tech_keywords: list, resume_tech_keywords: list):
    if not resume_tech_keywords or (not desc_tech_keywords and not title_tech_keywords):
        return 0

    def get_multiplier(keywords):
        try:
            return len([word for word in keywords if word in resume_tech_keywords]) / len(keywords)
        except ZeroDivisionError:
            return 0

    desc_multiplier = get_multiplier(desc_tech_keywords)
    title_multiplier = get_multiplier(title_tech_keywords)

    added_score = (title_multiplier * TITLE_KEYWORD_BONUS) + \
        (desc_multiplier * DESC_KEYWORD_BONUS)
    result = round(added_score, 5)

    return result


# checks for exact job title match and returns a bonus score to be added
def check_roles(candidate, job_title):

    if not candidate.resume_string:
        return 0

    title = clean_job_title(job_title).lower()
    resume = candidate.resume_string.lower()

    if title in resume:
        return 0.1
    else:
        return 0

# calculates the bonus score for a candidate based on the job


def calculate_bonus_score(job, candidate):
    bonus_score = 0
    bonus_score += check_roles(candidate, job.job_title)
    bonus_score += check_resume(job.desc_tech_keywords, job.title_tech_keywords,
                                candidate.tech_keywords)
    result = round(bonus_score, 5)
    return result
