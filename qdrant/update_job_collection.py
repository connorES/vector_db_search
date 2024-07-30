from qdrant_client.http import models
from qdrant.get_client import get_client
from database.queries import get_open_jobs
from utils.object_creator import create_jobs_from_list
from qdrant.create_points import prepare_points_job_id
from qdrant.upload_points import upload_points


def get_qdrant_job_ids(client, collection):
    job_ids_in_qdrant = set()
    scroll_result = client.scroll(
        collection_name=collection,
        scroll_filter=None,
        limit=150000,
        with_payload=True,
        with_vectors=False
    )

    for record in scroll_result[0]:
        job_ids_in_qdrant.add(record.id)

    return job_ids_in_qdrant


def main():
    client = get_client()
    collection = "open_jobs"
    open_jobs_list = get_open_jobs()
    open_job_ids = set(job['JobID'] for job in open_jobs_list)
    qdrant_job_ids = get_qdrant_job_ids(client, collection)

    # Identify jobs to remove
    jobs_to_remove = qdrant_job_ids - open_job_ids
    # Identify new jobs to add
    jobs_to_add = open_job_ids - qdrant_job_ids

    if not jobs_to_remove and not jobs_to_add:
        print("No changes needed in Qdrant")
        return

    # Remove outdated jobs
    if jobs_to_remove:
        print(f"Removing {len(jobs_to_remove)} outdated jobs from Qdrant...")
        client.delete(
            collection_name=collection,
            points_selector=models.PointIdsList(
                points=list(jobs_to_remove)
            )
        )

    # Add new jobs
    if jobs_to_add:
        print(f"Adding {len(jobs_to_add)} new jobs to Qdrant...")
        new_jobs_list = [job for job in open_jobs_list if job['JobID'] in jobs_to_add]
        new_jobs = create_jobs_from_list(new_jobs_list)
        print("Preparing points for Qdrant...")
        try:
            points = prepare_points_job_id(new_jobs)
        except Exception as e:
            print(f"Error preparing points: {e}")
            return
        print("Uploading points to Qdrant...")
        upload_points(client, collection, points)

    print("Qdrant update completed successfully")