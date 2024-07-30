from utils.bonus_score import clean_string
from utils.encode import encode_string
import math
import json


def prepare_points_cand_id(candidates, save_to_file=False):
    points = []
    print(f"Preparing {len(candidates)} points")
    for idx, candidate in enumerate(candidates):
        try:
            if math.isnan(candidate.candidate_class):
                candidate.candidate_class = 0

        except Exception as e:
            print(f"Error: {e}")
            candidate.candidate_class = 0

        cleaned_resume = clean_string(candidate.resume_string)
        embedding = encode_string(cleaned_resume)

        if cleaned_resume == "" or not cleaned_resume or embedding is None:
            print(f"Skipping candidate: {idx} {cleaned_resume} len cleaned resume: {len(cleaned_resume)},  len raw resume: { len(candidate.resume_string)} {candidate.name} {candidate.candidate_id} {type(candidate.security_clearance)} {candidate.location} {candidate.candidate_class}")
            continue

        points.append({
            'id': candidate.candidate_id,
            'vector': embedding,
            'payload': {'clearance': candidate.security_clearance,
                        'location': candidate.location,
                        'class': candidate.candidate_class,
                        'tech_keywords': candidate.tech_keywords,
                        'update_date': candidate.update_date
                        }
        })

    if save_to_file:
        save_points_to_file(points, "candidate_points.json")

    return points


def prepare_points_job_id(jobs, save_to_file=False):
    points = []
    for idx, job in enumerate(jobs):
        cleaned_description = clean_string(job.job_desc)
        embedding = encode_string(cleaned_description)

        if cleaned_description == "" or not cleaned_description or embedding is None:
            print(
                f"Skipping job: {idx} {cleaned_description} {type(cleaned_description)} {type(job.job_description)} {job.job_title} {job.job_id}")
            continue

        points.append({
            'id': int(job.job_id),
            'vector': embedding,
            'payload': {'title': job.job_title,
                        'location': job.location,
                        'clearance': job.clearance,
                        'manager': job.manager,
                        'closing_date': job.closing_date,
                        'client': job.client,
                        'tech_keywords': job.title_tech_keywords + job.desc_tech_keywords                        
                        }
        })

    if save_to_file:
        save_points_to_file(points, "job_points.json")

    return points


def save_points_to_file(points, file_path):
    with open(file_path, 'w') as file:
        json.dump(points, file, indent=2)
