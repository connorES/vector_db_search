from database.queries import get_linked_candidates
from qdrant.search import get_client
from qdrant.create_points import prepare_points_cand_id
from qdrant.upload_points import upload_points
from utils.object_creator import create_cands_from_list


def get_linked_cands(job_id):
    candidates = get_linked_candidates(str(job_id))
    
    # Create a set of unique candidate IDs
    unique_candidate_ids = set()
    unique_candidates = []

    for candidate in candidates:
        candidate_id = candidate['CandidateID']
        if candidate_id not in unique_candidate_ids:
            unique_candidate_ids.add(candidate_id)
            unique_candidates.append(candidate)

    return unique_candidate_ids, unique_candidates


def get_qdrant_cand_ids(client, collection):
    candidate_ids_in_qdrant = set()
    scroll_result = client.scroll(
        collection_name=collection,
        scroll_filter=None,
        limit=150000,
        with_payload=True,
        with_vectors=False
    )

    for record in scroll_result[0]:
        candidate_ids_in_qdrant.add(record.id)

    return candidate_ids_in_qdrant


def upload_new_linked_cands(job):
    client = get_client()
    collection_name = "wide_cands"
    linked_cand_ids, linked_cands = get_linked_cands(job.job_id)
    job.linked_candidate_ids = linked_cand_ids
    qdrant_ids = get_qdrant_cand_ids(client, collection_name)
    new_cands = linked_cand_ids - qdrant_ids
    
    if len(new_cands) == 0:
        print("No new candidates to upload")
        return
    
    # Filter new candidates
    new_cands_list = [cand for cand in linked_cands if cand['CandidateID'] in new_cands]
    
    # Remove duplicates based on CandidateID
    seen_ids = set()
    unique_new_cands = []
    for cand in new_cands_list:
        if cand['CandidateID'] not in seen_ids:
            seen_ids.add(cand['CandidateID'])
            unique_new_cands.append(cand)
    
    # Create candidate objects
    new_cands_objects = create_cands_from_list(unique_new_cands)
    
    # Prepare points and upload
    points = prepare_points_cand_id(new_cands_objects, save_to_file=False)
    upload_points(client, collection_name, points)