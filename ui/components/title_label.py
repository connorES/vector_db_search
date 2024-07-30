from customtkinter import CTkLabel

class TitleLabel:
    def __init__(self, frame, text):
        self.text = text
        self.frame = frame
        self.label = self.create_label()

    def create_label(self):
        label = CTkLabel(master=self.frame, text=self.text,
                         font=("Helvetica", 18, "bold"))
        label.pack(pady=20, padx=10)
        return label
