from qdrant_client.http import models
from database.queries import get_hot_candidates
from utils.object_creator import create_cands_from_list
from qdrant.create_points import prepare_points_cand_id
from qdrant.upload_points import upload_points
from qdrant.get_client import get_client


def get_qdrant_hot_cands_ids(client, collection):
    hot_cands_ids_in_qdrant = set()
    scroll_result = client.scroll(
        collection_name=collection,
        scroll_filter=None,
        limit=150000,
        with_payload=True,
        with_vectors=False
    )
    for record in scroll_result[0]:
        hot_cands_ids_in_qdrant.add(record.id)
    return hot_cands_ids_in_qdrant


def main():
    client = get_client()
    collection = "hot_cands"

    print("Getting hot candidates from database...")
    hot_cands_list  = get_hot_candidates()
    hot_cands_ids = set(cand['CandidateID'] for cand in hot_cands_list)

    print("Getting hot candidate IDs from Qdrant...")
    qdrant_hot_cands_ids = get_qdrant_hot_cands_ids(client, collection)

    # Identify candidates to remove
    cands_to_remove = qdrant_hot_cands_ids - hot_cands_ids
    # Identify new candidates to add
    cands_to_add = hot_cands_ids - qdrant_hot_cands_ids

    if not cands_to_remove and not cands_to_add:
        print("No changes needed in Qdrant")
        return

    # Remove outdated candidates
    if cands_to_remove:
        print(
            f"Removing {len(cands_to_remove)} outdated candidates from Qdrant...")
        client.delete(
            collection_name=collection,
            points_selector=models.PointIdsList(
                points=list(cands_to_remove)
            )
        )

    # Add new candidates
    if cands_to_add:
        print(f"Adding {len(cands_to_add)} new candidates to Qdrant...")
        new_cands_list = [cand for cand in hot_cands_list if cand['CandidateID'] in cands_to_add]
        new_candidates = create_cands_from_list(new_cands_list)

        print("Preparing points for Qdrant...")
        try:
            points = prepare_points_cand_id(new_candidates)
        except Exception as e:
            print(f"Error preparing points: {e}")
            return

        print("Uploading points to Qdrant...")
        upload_points(client, collection, points)

    print("Qdrant update completed successfully")


if __name__ == "__main__":
    main()
