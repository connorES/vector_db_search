from customtkinter import CTkComboBox
from utils.constants import RECRUITERS

class RecruiterNameSelect:
    def __init__(self, frame):
        self.frame = frame
        self.create()

    def create(self):
        dropdown = CTkComboBox(master=self.frame, values=RECRUITERS)
        dropdown.pack(pady=10, padx=10, anchor="c")
        self.dropdown = dropdown

    def get(self):
        return self.dropdown.get()
