from customtkinter import CTkFrame, CTkLabel, CTkEntry


class PasteInputText:
    def __init__(self, master, label_text, placeholder_text):
        self.master = master
        self.label_text = label_text
        self.placeholder_text = placeholder_text
        self.id_entry = None
        self.create_input()

    def create_input(self):
        # Create a frame to hold the ID label and entry field
        id_frame = CTkFrame(master=self.master)
        id_frame.pack(pady=10, padx=10, anchor="c")

        id_label = CTkLabel(master=id_frame,
                            text=self.label_text, font=("Helvetica", 12, "bold"))
        id_label.grid(row=0, column=0, padx=(0, 5), sticky="e")

        # Add the job ID entry field
        id_entry = CTkEntry(
            master=id_frame, placeholder_text=self.placeholder_text)
        id_entry.grid(row=0, column=1, sticky="w")

        self.id_entry = id_entry

    def get(self):
        return self.id_entry.get()
