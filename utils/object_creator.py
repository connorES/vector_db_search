from utils.constants import ORIGINAL_RESUMES_FILEPATH
from classes.job import Job
from classes.candidate import Candidate
from utils.language_scoring import find_langs
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import cpu_count

def create_candidate(cand_dict):
    cand = Candidate(cand_dict["CandidateID"])
    cand.resume_path = ORIGINAL_RESUMES_FILEPATH + cand_dict["CandDocPath"]
    cand.set_clearance(cand_dict["SecurityClearanceName"])
    cand.tris_data = cand_dict["CandidateInfo"]
    cand.candidate_class = cand_dict["CandidateClass"]
    cand.update_date = cand_dict["CandDocUpdateDate"]
    cand.set_location()
    cand.add_text()
    cand.tech_keywords = find_langs(cand.resume_string)

    return cand

def create_cands_from_list(candidates_list, num_processes=None):
    print(f"Creating {len(candidates_list)} candidates")
    if not candidates_list:
        return []

    if num_processes is None:
        num_processes = cpu_count()

    candidates = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        future_to_candidate = {executor.submit(create_candidate, cand_dict) 
                               for idx, cand_dict in enumerate(candidates_list)}
        
        for future in as_completed(future_to_candidate):
            candidate = future.result()
            candidates.append(candidate)

    return candidates


def create_jobs_from_list(jobs_list):
    if not jobs_list:
        return []

    def create_job(job_dict):
        job = Job(job_dict["JobID"])
        job.job_desc = job_dict["JobMainSkills"] + job_dict["JobTechnicalNotes"]
        job.manager = job_dict["AMName"]
        job.job_title = job_dict["JobTitle"]
        job.location = job_dict["JobLocation"]
        job.closing_date = job_dict["JobClosingDate"]
        job.client = job_dict["ClientName"]
        job.set_clearance()
        job.set_location()
        job.title_tech_keywords = find_langs(job.job_title)
        job.desc_tech_keywords = find_langs(job.job_desc)
        return job
    
    return [create_job(job_dict) for job_dict in jobs_list]
