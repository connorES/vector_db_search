from utils.threading import start_thread
from ui.qdrant_functions import rec_review
from customtkinter import CTkFrame
from ui.components.title_label import TitleLabel
from ui.components.input.recruiter_dropdown import RecruiterNameSelect
from ui.components.input.filter_panel import FilterPanel
from ui.components.input.action_button import ActionButton
from ui.components.input.progress_bar import ProgressBar
import traceback

class RecReviewFrame:
    def __init__(self, parent_frame):
        self.frame = CTkFrame(master=parent_frame)
        self.frame.pack(pady=30, padx=40, side="right",
                        expand=True, fill="both")
        self.parent_frame = parent_frame
        self.create_widgets()

    def create_widgets(self):
        self.title = TitleLabel(self.frame, "Recruiter Review")
        self.dropdown = RecruiterNameSelect(self.frame)
        self.filters = FilterPanel(self.frame, filters=['location', 'clearance'])
        self.search_button = ActionButton(self.frame, "Find Jobs", self.rank_candidates)
        self.progress_bar = ProgressBar(self.frame)

    def rank_candidates(self):
        filters = self.filters.get_selected_filters()
        recruiter_name = self.dropdown.get()

        # Start the recruiter review in a separate thread
        start_thread(self.run_recruiter_review, recruiter_name, filters)

    def run_recruiter_review(self, recruiter_name, filters):
        try:
            rec_review(self.frame, recruiter_name, filters, self.progress_bar)
        except Exception as e:
            print(traceback.format_exc())   
            print(f"Error during recruiter review: {e}")
            return