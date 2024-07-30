from customtkinter import CTkFrame
from utils.threading import start_thread
from ui.qdrant_functions import find_cands
from ui.components.title_label import TitleLabel
from ui.components.input.id_input import IdInput
from ui.components.input.filter_panel import FilterPanel
from ui.components.input.action_button import ActionButton
from ui.components.input.progress_bar import ProgressBar
from ui.components.input.msg_box import msg_box

class FindCandFrame(CTkFrame):
    def __init__(self, parent_frame):
        self.frame = CTkFrame(master=parent_frame)
        self.frame.pack(pady=30, padx=40, side="right",
                        expand=True, fill="both")
        self.parent_frame = parent_frame
        self.create_widgets()

    def create_widgets(self):
        self.title = TitleLabel(self.frame, "Candidate Search")
        self.id_input = IdInput(self.frame, "Job ID: ", "Enter Job ID or Paste JD")
        self.id_input.bind_enter(self.find_candidates)
        self.filters = FilterPanel(self.frame, filters=['location', 'clearance'])
        self.search_button = ActionButton(self.frame, "Find Candidates", self.find_candidates)
        self.progress_bar = ProgressBar(self.frame)
    
    def on_enter(self, event):
        if "\n" not in self.id_input.get():
            self.find_candidates()
        else:
            return "break"

    def find_candidates(self):
        job_id = self.id_input.get()
        filters = self.filters.get_selected_filters()

        # Start the search in a separate thread
        start_thread(self.run_search, job_id, filters)

    def run_search(self, job_id, filters):
        try:
            create_results_frame = find_cands(self.frame, job_id, filters, self.progress_bar)
            if create_results_frame:
                self.frame.after(100, self.show_results, create_results_frame)
        except Exception as e:
            msg_box(f"Error during candidate search: {e}", self.frame).delayed_destroy()
            if self.progress_bar.is_running:
                self.progress_bar.stop()

    def show_results(self, create_results_frame):
        create_results_frame()
        if self.progress_bar.is_running:
                self.progress_bar.stop()