from ui.components.results.qdrant_candidate_results_table import QdrantCandidateResultsTable
from ui.components.results.results_search_info_panel import ResultsSearchInfoPanel
from utils.constants import ICON_PATH
from ui.frames.results.expandable_frame import ExpandableFrame
import customtkinter as ctk


class RecruiterReviewResultsFrame(ctk.CTkToplevel):
    def __init__(self, recruiter_results, rec_name, filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recruiter_results = recruiter_results
        self.filters = filters
        self.geometry("1080x800")
        self.title(f"Recruiter Review: {rec_name}")
        self.after(250, lambda: self.iconbitmap(ICON_PATH))
        self.create_widgets()
        self.after(1, lambda: self.focus_force())

    def create_widgets(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        for job_id, job_results in self.recruiter_results.items():

            job_title = job_results['job'].job_title
            keywords = job_results['job'].title_tech_keywords + job_results['job'].desc_tech_keywords

            job_frame = ExpandableFrame(
                self.scrollable_frame, f"{job_title} {job_id}"
            )
            job_frame.pack(fill="x", padx=10, pady=5)

            content_frame = job_frame.get_content_frame()

            self.job_info_panel = ResultsSearchInfoPanel(
                content_frame, job_results['job'], filters=self.filters
            )

            if job_results['hot_cand_results'] != []:

                hot_cands_frame = ExpandableFrame(
                    content_frame, "Top 10 Hot Candidates"
                )
                hot_cands_frame.pack(fill="x", padx=10, pady=5)
                hot_cands_content = hot_cands_frame.get_content_frame()
                hot_cands_sheet = QdrantCandidateResultsTable(
                    master=hot_cands_content,
                    results=job_results['hot_cand_results'],
                    keywords=keywords,
                    height=290
                )
                hot_cands_sheet.sheet.pack(
                    padx=10, pady=10, fill="both", expand=True)

            if job_results['wide_cand_results'] != []:
                wide_cands_frame = ExpandableFrame(
                    content_frame, "Top 100 TRIS Candidates"
                )
                wide_cands_frame.pack(fill="x", padx=10, pady=5)
                wide_cands_content = wide_cands_frame.get_content_frame()
                wide_cands_sheet = QdrantCandidateResultsTable(
                    master=wide_cands_content,
                    results=job_results['wide_cand_results'],
                    keywords=keywords
                )
                wide_cands_sheet.sheet.pack(
                    padx=10, pady=10, fill="both", expand=True)
