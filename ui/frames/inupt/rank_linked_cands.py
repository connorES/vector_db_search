from customtkinter import CTkFrame
from utils.threading import start_thread
from ui.qdrant_functions import rank_linked_cands
from ui.components.title_label import TitleLabel
from ui.components.input.id_input import IdInput
from ui.components.input.filter_panel import FilterPanel
from ui.components.input.action_button import ActionButton
from ui.components.input.progress_bar import ProgressBar
from ui.components.input.msg_box import msg_box
import traceback

class RankLinkedCandsFrame:
    def __init__(self, parent_frame):
        self.frame = CTkFrame(master=parent_frame)
        self.frame.pack(pady=30, padx=40, side="right", expand=True, fill="both")
        self.parent_frame = parent_frame
        self.create_widgets()

    def create_widgets(self):
        self.title = TitleLabel(self.frame, "Rank Linked Candidates")
        self.id_input = IdInput(self.frame, "Job ID: ", "Enter Job ID")
        self.id_input.bind_enter(self.rank_candidates)
        self.filters = FilterPanel(self.frame, filters=['location', 'clearance'])
        self.search_button = ActionButton(self.frame, "Rank Linked Candidates", self.rank_candidates)
        self.progress_bar = ProgressBar(self.frame)

    def rank_candidates(self):
        job_id = self.id_input.get()
        filters = self.filters.get_selected_filters()

        # Start the ranking in a separate thread
        start_thread(self.run_ranking, job_id, filters)


    def run_ranking(self, job_id, filters):
        try:
            rank_linked_cands(self.frame, job_id, filters, self.progress_bar)
        except Exception as e:
            print(traceback.format_exc())
            # Schedule error message to be shown on the main thread
            self.frame.after(0, self.show_error_message, str(e))
        finally:
            # Ensure the progress bar is reset on the main thread
            self.frame.after(0, self.progress_bar.stop())

    def show_error_message(self, error_msg):
        msg_box(f"An error occurred during candidate ranking:{error_msg}", self.frame).delayed_destroy()
