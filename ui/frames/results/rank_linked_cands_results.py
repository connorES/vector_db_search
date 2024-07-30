from customtkinter import CTkToplevel, CTkFrame, CTkLabel
from ui.components.results.qdrant_candidate_results_table import QdrantCandidateResultsTable
from ui.components.results.results_search_info_panel import ResultsSearchInfoPanel
from utils.constants import ICON_PATH


class RankLinkedCandsResults(CTkToplevel):
    def __init__(self, results, job, filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = job
        self.filters = filters
        self.results = results
        self.title(f"Ranked Linked Canidates for {job.job_title}")
        self.geometry("1080x800")
        self.after(250, lambda: self.iconbitmap(ICON_PATH))
        self.results_frame = CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()
        self.after(1, lambda: self.focus_force())

    def create_widgets(self):
        # Create a frame for the job information
        self.job_info_panel = ResultsSearchInfoPanel(
            self.results_frame, self.job, filters=self.filters)

        self.db_search_label = CTkLabel(
            self.results_frame, text="Linked Candidates", font=("Arial", 16, "bold"))
        self.db_search_label.pack(pady=(10, 5), padx=10, anchor="w")

        # # Create the table in the upper panel
        self.sheet = QdrantCandidateResultsTable(
            master=self.results_frame,
            results=self.results,
            keywords=self.job.title_tech_keywords + self.job.desc_tech_keywords
        )
        self.sheet.sheet.pack(padx=10, pady=(5, 10), fill="both", expand=True)
