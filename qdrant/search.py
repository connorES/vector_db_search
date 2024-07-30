from utils.encode import encode_string
from qdrant_client.http.models import FieldCondition, MatchAny, HasIdCondition, DatetimeRange
from qdrant_client.models import Filter
from utils.bonus_score import clean_string
from qdrant.get_client import get_client
from utils.bonus_score import add_bonus_score
from utils.constants import ORIGINAL_RESUMES_FILEPATH
from database.queries import get_multiple_candidates
from classes.job import Job
from datetime import datetime, timedelta


def search_candidates(filters=None, input=None, search_linked_cands=False):

    if isinstance(input, str):
        query_vector = encode_string(input)
        filters = Filter()

    elif isinstance(input, Job):
        query_vector = encode_string(input.job_title + " " + input.job_desc)
        filters = get_filter(input, filters, search_linked_cands)

    wide_cand_results = search_wide_cands(query_vector=query_vector, filters=filters, input=input)

    if search_linked_cands:
        hot_cand_results = None
    else:
        hot_cand_results = search_hot_cands(query_vector=query_vector, filters=filters, input=input)

    results = {
        "wide_cand_results": wide_cand_results,
        "hot_cand_results": hot_cand_results
    }

    return results


def search_wide_cands(filters=None, query_vector=None, input=None):

    client = get_client()
    collection = "wide_cands_fe"

    results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        query_filter=filters,
        limit=100
    )

    results = add_bonus_score(input, results)
    add_candidate_data(results)
    return results


def search_hot_cands(filters=None, query_vector=None, input=None):

    client = get_client()
    collection = "hot_cands"

    results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        query_filter=filters,
        limit=10
    )

    results = add_bonus_score(input, results)
    add_candidate_data(results)
    return results


def search_open_jobs(candidate=None, query_string=None):
    client = get_client()
    collection = "open_jobs"

    if candidate:
        cleaned_resume = clean_string(candidate.resume_string)
        query_vector = encode_string(cleaned_resume)
        input = candidate

    if query_string:
        cleaned_string = clean_string(query_string)
        query_vector = encode_string(cleaned_string)
        input = cleaned_string

    results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=100
    )

    results = add_bonus_score(input, results)
    return results


def add_candidate_data(results):
    # Create a mapping of result IDs to their index in the results list
    id_to_index = {result[0].id: index for index, result in enumerate(results)}

    # Get candidate data for all IDs at once
    candidates_list = get_multiple_candidates(list(id_to_index.keys()))

    for candidate in candidates_list:
        candidate_id = candidate['CandidateID']
        if candidate_id in id_to_index:
            index = id_to_index[candidate_id]
            payload = results[index][0].payload
            payload['name'] = f"{candidate['PersonFirstName']} {candidate['PersonSurname']}"
            payload['path'] = ORIGINAL_RESUMES_FILEPATH + candidate['CandDocPath']
            payload['current_role'] = candidate['CurrentPosition']
            payload['last_updated'] = candidate['CandDocUpdateDate']

    return results


# construct qdrant filters
def get_filter(obj, filters, linked_cands_only=False):

    filter_list = []

    if linked_cands_only:
        linked_cands_filter = HasIdCondition(has_id=obj.linked_candidate_ids)
        filter_list.append(linked_cands_filter)
    elif filters['cv_update'] != "Any":
        date_filter = get_date_filter(filters['cv_update'])
        filter_list.append(date_filter)

    if filters is None and not linked_cands_only:
        return Filter()

    if filters['location']:
        location_filter = FieldCondition(
            key="location", match=MatchAny(any=obj.location))
        filter_list.append(location_filter)

    if filters['clearance']:
        clearance_filter = FieldCondition(
            key="clearance", match=MatchAny(any=obj.get_clearances()))
        filter_list.append(clearance_filter)

    filter = Filter(
        must=filter_list
    )

    return filter

def get_date_filter(dropdown_option):
    num_months = int(dropdown_option.split(" ")[0])
    cutoff_date = datetime.now() - timedelta(days=30 * num_months)

    return FieldCondition(
        key = "update_date", 
        range = DatetimeRange(
            gte=cutoff_date.isoformat()
        )
    )
