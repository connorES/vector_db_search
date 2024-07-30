from customtkinter import CTkToplevel, CTkFrame, CTkLabel
from ui.components.results.qdrant_job_results_table import QdrantJobResultsTable
from ui.components.results.results_cand_info_panel import ResultsCandInfoPanel
from utils.constants import ICON_PATH


class SearchJobsResults(CTkToplevel):
    def __init__(self, results, candidate=None, input_keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate = candidate
        self.set_keywords(input_keywords)
        self.results = results
        self.geometry("1080x800")
        self.after(250, lambda: self.iconbitmap(ICON_PATH))
        self.results_frame = CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()
        self.after(1, lambda: self.focus_force())

    def set_keywords(self, keywords):
        if self.candidate is not None:
            self.keywords = self.candidate.tech_keywords
        elif keywords is not None:
            self.keywords = keywords

    def create_widgets(self):

        if self.candidate is not None:
            # Create a frame for the job information
            self.job_info_panel = ResultsCandInfoPanel(
                self.results_frame, self.candidate, filters=None)

        self.db_search_label = CTkLabel(
            self.results_frame, text="Open Jobs", font=("Arial", 16, "bold"))
        self.db_search_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.sheet = QdrantJobResultsTable(
            master=self.results_frame,
            results=self.results,
            keywords=self.keywords
        )
        self.sheet.sheet.pack(padx=10, pady=(5, 10), fill="both", expand=True)
