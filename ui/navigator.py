from customtkinter import CTkFrame
from ui.frames.inupt.cand_search import FindCandFrame
from ui.frames.inupt.rank_linked_cands import RankLinkedCandsFrame
from ui.frames.inupt.find_jobs import FindJobsFrame
from ui.frames.inupt.recruiter_review import RecReviewFrame
from ui.frames.sidebar import Sidebar


class Navigator:
    def __init__(self, root_frame):
        self.root_frame = root_frame
        self.main_panel = None
        self.sidebar = None
        self.initialize_layout()

    def initialize_layout(self):
        # Create a persistent sidebar
        sidebar_frame = CTkFrame(
            self.root_frame, width=200, corner_radius=0, fg_color="gray13")
        sidebar_frame.pack(side="left", fill="y", expand=False)
        self.sidebar = Sidebar(sidebar_frame, self)

        # Create a main panel that will be updated
        self.main_panel = CTkFrame(self.root_frame)
        self.main_panel.pack(side="right", fill="both", expand=True)

    def navigate_to(self, frame_class):
        # Clear only the main panel
        for widget in self.main_panel.winfo_children():
            widget.destroy()
        # Create the new frame in the main panel
        frame_class(self.main_panel)

    def open_find_cand(self):
        self.navigate_to(FindCandFrame)
        self.sidebar.update_selected(self.sidebar.buttons[0])

    def open_rank_cand(self):
        self.navigate_to(RankLinkedCandsFrame)
        self.sidebar.update_selected(self.sidebar.buttons[1])

    def open_find_jobs(self):
        self.navigate_to(FindJobsFrame)
        self.sidebar.update_selected(self.sidebar.buttons[2])

    def open_rec_review(self):
        self.navigate_to(RecReviewFrame)
        self.sidebar.update_selected(self.sidebar.buttons[3])
