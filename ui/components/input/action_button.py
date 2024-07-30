from customtkinter import CTkButton

class ActionButton:
    def __init__(self, master, text, command):
        self.master = master
        self.text = text
        self.command = command
        self.create_button()

    def create_button(self):
        button = CTkButton(master=self.master, text=self.text,
                            command=self.command, font=("Helvetica", 14, "bold"))
        button.pack(pady=30, padx=10, anchor="c")
        return button