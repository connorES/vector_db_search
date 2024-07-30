from ui.components.results.qdrant_candidate_results_table import QdrantCandidateResultsTable
from ui.components.results.results_search_info_panel import ResultsSearchInfoPanel
from utils.constants import ICON_PATH
from ui.frames.results.expandable_frame import ExpandableFrame
import customtkinter as ctk


class CandSearchResultsFrame(ctk.CTkToplevel):
    def __init__(self, results=None, filters=None, hot_cand_results=None, job=None, job_keywords=None, input_string=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = job
        self.results = results
        self.filters = filters
        self.input_string = input_string
        self.hot_cand_results = hot_cand_results
        self.set_title()
        self.set_keywords(job_keywords)
        self.geometry("1080x900")
        self.after(250, lambda: self.iconbitmap(ICON_PATH))
        self.create_widgets()
        self.after(1, lambda: self.focus_force())

    def set_keywords(self, keywords):
        if self.job is not None:
            self.keywords = self.job.title_tech_keywords + self.job.desc_tech_keywords
        elif keywords is not None:
            self.keywords = keywords

    def set_title(self):
        if self.job is not None:
            self.title(f"{self.job.job_title} {self.job.job_id}")
        else:
            self.title("Custom Search Results")

    def create_widgets(self):
        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create the job information panel at the top
        self.job_info_panel = ResultsSearchInfoPanel(
            self.scrollable_frame, job=self.job, keywords=self.keywords, input_string=self.input_string, filters=self.filters)

        if self.hot_cand_results is not None:
            # Create expandable frame for Hot Candidates
            self.hot_cands_frame = ExpandableFrame(
                self.scrollable_frame, "Top 10 Hot Candidates")
            self.hot_cands_frame.pack(fill="x", padx=10, pady=5)

            content_frame = self.hot_cands_frame.get_content_frame()
            self.hot_cands_sheet = QdrantCandidateResultsTable(
                master=content_frame,
                results=self.hot_cand_results,
                keywords=self.keywords,
                height=290
            )
            self.hot_cands_sheet.sheet.pack(
                padx=10, pady=10, fill="both", expand=True)

        if self.results is not None:
            # Create expandable frame for TRIS Candidates
            self.tris_cands_frame = ExpandableFrame(
                self.scrollable_frame, "Top 100 TRIS Candidates")
            self.tris_cands_frame.pack(fill="x", padx=10, pady=5)

            content_frame = self.tris_cands_frame.get_content_frame()
            self.sheet = QdrantCandidateResultsTable(
                master=content_frame,
                results=self.results,
                keywords=self.keywords,
            )
            self.sheet.sheet.pack(padx=10, pady=10, fill="both", expand=True)
