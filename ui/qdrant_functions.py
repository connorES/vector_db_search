from utils.object_creator import create_jobs_from_list, create_cands_from_list
from utils.bonus_score import find_langs
from database.queries import get_single_job, get_open_jobs_recruiter, get_single_candidate
from qdrant.search import search_open_jobs, search_candidates
from qdrant.get_new_cands import upload_new_linked_cands
from qdrant.update_job_collection import main as update_job_collection
from qdrant.update_hot_cands_collection import main as update_hot_cands_collection
from utils.input_validation import validate_int
from utils.threading import start_thread
from ui.components.input.msg_box import msg_box
from ui.frames.results.cand_search_results import CandSearchResultsFrame
from ui.frames.results.rank_linked_cands_results import RankLinkedCandsResults
from ui.frames.results.search_job_results import SearchJobsResults
from ui.frames.results.rec_review_results import RecruiterReviewResultsFrame


def find_cands(frame, input_string, filters, progress_bar):

    if input_string.isdigit():
        if not validate_int(input_string):
            msg_box("Please enter a valid Job ID", frame).delayed_destroy()
            return
    elif input_string is None or input_string == "":
        msg_box("Please enter a valid Job ID", frame).delayed_destroy()
        return

    progress_bar.start()
    
    update_progress(10, progress_bar)
    update_hot_cands_collection()

    def create_results_frame(results, **kwargs):
        return lambda: CandSearchResultsFrame(
            results=results['wide_cand_results'],
            hot_cand_results=results['hot_cand_results'],
            **kwargs
        )

    if input_string.isdigit():
        # Job ID search list
        job_df = get_single_job(input_string)
        update_progress(20, progress_bar)

        job = create_jobs_from_list(job_df)[0]
        update_progress(60, progress_bar)

        results = search_candidates(input=job, filters=filters)
        update_progress(100, progress_bar)

        return create_results_frame(results, filters=filters, job=job)
    else:
        # Keyword search path
        keywords = find_langs(input_string)
        update_progress(20, progress_bar)

        results = search_candidates(input=input_string)
        update_progress(80, progress_bar)

        return create_results_frame(results, job_keywords=keywords, input_string=input_string)


def rank_linked_cands(frame, jobID, filters, progress_bar):
    if not jobID.isdigit():
        msg_box("Please enter a valid Job ID", frame).delayed_destroy()
        return

    if not validate_int(jobID):
        msg_box("Please enter a valid Job ID", frame).delayed_destroy()
        return

    progress_bar.start()
    update_progress(10, progress_bar)

    job_df = get_single_job(jobID)
    update_progress(30, progress_bar)
    
    job = create_jobs_from_list(job_df)[0]
    update_progress(50, progress_bar)

    upload_new_linked_cands(job)
    update_progress(70, progress_bar)

    results = search_candidates(input=job, filters=filters, search_linked_cands=True)
    update_progress(90, progress_bar)

    RankLinkedCandsResults(results['wide_cand_results'], job, filters)
    update_progress(100, progress_bar)

    progress_bar.stop()



def find_jobs(frame, input_string, progress_bar):
    if input_string.isdigit():
        if not validate_int(input_string):
            msg_box("Please enter a valid Candidate ID", frame).delayed_destroy()
            return
    elif input_string is None or input_string == "":
        msg_box("Please enter a valid Candidate ID", frame).delayed_destroy()
        return

    progress_bar.start()

    update_progress(10, progress_bar)
    update_job_collection()

    update_progress(20, progress_bar)
    update_hot_cands_collection()

    
    if not input_string.isdigit():
        # Keyword search path
        update_progress(40, progress_bar)
        input_keywords = find_langs(input_string)
        
        update_progress(60, progress_bar)
        results = search_open_jobs(query_string=input_string)
        
        update_progress(80, progress_bar)
        SearchJobsResults(results, input_keywords=input_keywords)

        update_progress(100, progress_bar)
        progress_bar.stop()
    else:
        # Candidate ID search path
        update_progress(20, progress_bar)
        cand_df = get_single_candidate(input_string)
        
        if len(cand_df) == 0:
            msg_box("Candidate not found", frame).delayed_destroy()
            progress_bar.stop()
            return

        update_progress(40, progress_bar)
        candidate = create_cands_from_list(cand_df)
        
        update_progress(60, progress_bar)
        results = search_open_jobs(candidate=candidate[0])

        update_progress(80, progress_bar)
        SearchJobsResults(results, candidate=candidate[0])

        update_progress(100, progress_bar)
        progress_bar.stop()


def rec_review(frame, rec_name, filters, progress_bar):
    recruiter_results = {}
    progress_bar.start()

    update_progress(5, progress_bar)
    update_job_collection()

    update_progress(10, progress_bar)
    update_hot_cands_collection()

    update_progress(20, progress_bar)
    recruiter_open_jobs_df = get_open_jobs_recruiter(rec_name)

    update_progress(30, progress_bar)
    recruiter_open_jobs = create_jobs_from_list(recruiter_open_jobs_df)

    total_jobs = len(recruiter_open_jobs)
    for index, job in enumerate(recruiter_open_jobs):
        results = search_candidates(input=job, filters=filters)
        recruiter_results[job.job_id] = {
            'job': job,
            'wide_cand_results': results['wide_cand_results'],
            'hot_cand_results': results['hot_cand_results']
        }
        # Update progress based on the number of jobs processed
        update_progress(30 + (60 * (index + 1) / total_jobs), progress_bar)

    update_progress(90, progress_bar)
    frame.after(0, lambda: RecruiterReviewResultsFrame(
        recruiter_results, rec_name, filters))

    update_progress(100, progress_bar)
    progress_bar.stop()


def refresh_qdrant_jobs(frame):
    msg = msg_box("Refreshing open jobs...", frame)
    start_thread(update_job_collection)
    msg.delayed_msg("Jobs up to date.")
    msg.delayed_destroy()


def refresh_qdrant_hot_cands(frame):
    msg = msg_box("Refreshing hot candidates...", frame)
    start_thread(update_hot_cands_collection)
    msg.delayed_msg("Hot candidates up to date.")
    msg.delayed_destroy()


def update_progress(percentage, progress_bar):
    progress_bar.set(percentage)
