from utils.threading import start_thread
from ui.qdrant_functions import find_jobs
from customtkinter import CTkFrame
from ui.components.title_label import TitleLabel
from ui.components.input.id_input import IdInput
from ui.components.input.action_button import ActionButton
from ui.components.input.progress_bar import ProgressBar
from ui.components.input.msg_box import msg_box
import traceback

class FindJobsFrame:
    def __init__(self, parent_frame):
        self.frame = CTkFrame(master=parent_frame)
        self.frame.pack(pady=30, padx=40, side="right", expand=True, fill="both")
        self.parent_frame = parent_frame
        self.create_widgets()

    def create_widgets(self):
        self.title = TitleLabel(self.frame, "Rank Open Jobs for a Candidate")
        self.id_input = IdInput(self.frame, "Candidate ID: ", "Enter ID or Paste CV")
        self.id_input.bind_enter(self.find_jobs)
        self.search_button = ActionButton(self.frame, "Rank Jobs", self.find_jobs)
        self.progress_bar = ProgressBar(self.frame)

    def find_jobs(self):
        candidate_id = self.id_input.get()
        # Start the job search in a separate thread
        start_thread(self.run_job_search, candidate_id)

    def run_job_search(self, candidate_id):
        try:
            find_jobs(self.frame, candidate_id, self.progress_bar)
        except Exception as e:
            print(traceback.format_exc())
            msg_box(f"Error Finding Jobs", self.frame).delayed_destroy()
