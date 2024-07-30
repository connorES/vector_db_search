from ui.components.sidebar.sidebar_function_button import SidebarFunctionButton
from customtkinter import CTkFrame
import webbrowser 


class Sidebar:
    def __init__(self, parent_frame, navigator):
        self.parent_frame = parent_frame
        self.navigator = navigator
        self.buttons = []
        self.create_sidebar()

    def create_sidebar(self):
        button_data = [
            ("Candidate Search", self.navigator.open_find_cand),
            ("Rank Linked Candidates", self.navigator.open_rank_cand),
            ("Open Job Search", self.navigator.open_find_jobs),
            ("Recruiter Review", self.navigator.open_rec_review)
        ]

        for text, command in button_data:
            button = SidebarFunctionButton(self.parent_frame, text, command)
            button.pack(pady=5, padx=5)
            self.buttons.append(button)

        # Set the initial selected button
        self.update_selected(self.buttons[0])
        self.create_bottom_frame()

    def update_selected(self, selected_button):
        for button in self.buttons:
            button.set_selected(button == selected_button)

    def create_bottom_frame(self):
        bottom_frame = CTkFrame(self.parent_frame)
        bottom_frame.pack(side="bottom", fill="x")

        def open_help_wiki():
            webbrowser.open("https://www.notion.so/RHAI-Search-cc7ebe32765f4a9d80c0ecc7b9d471e9")

        button = SidebarFunctionButton(bottom_frame, "Help", open_help_wiki)
        button.button.configure(width=410, height=80, font=("Helvetica", 14), fg_color="transparent", text_color="white",  hover_color="gray20")
        button.pack(pady=5, padx=5)
