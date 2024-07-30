import customtkinter as ctk


class ExpandableFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.expanded = False
        self.content_frame = None
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.grid(row=0, column=0, sticky="ew")
        self.title_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text=f"▶ {self.title}",
            font=("Arial", 14, "bold"),
            anchor="w",
            padx=10,
            pady=5
        )
        self.title_label.grid(row=0, column=0, sticky="ew")

        self.title_frame.bind("<Button-1>", self.toggle)
        self.title_label.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        if self.expanded:
            self.content_frame.grid_forget()
            self.expanded = False
            self.title_label.configure(text=f"▶ {self.title}")
        else:
            if not self.content_frame:
                self.content_frame = ctk.CTkFrame(self)
            self.content_frame.grid(
                row=1, column=0, sticky="nsew", padx=10, pady=5)
            self.expanded = True
            self.title_label.configure(text=f"▼ {self.title}")

    def get_content_frame(self):
        if not self.content_frame:
            self.content_frame = ctk.CTkFrame(self)
        return self.content_frame
