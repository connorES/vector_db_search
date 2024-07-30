from customtkinter import CTkFrame, CTkLabel


class ResultsCandInfoPanel:
    def __init__(self, master, candidate, filters=None):
        self.master = master
        self.candidate = candidate
        self.filters = filters
        self.frame = self.create_frame()
        self.add_info()

    def create_frame(self):
        filters_frame = CTkFrame(master=self.master)
        filters_frame.pack(pady=20, padx=10, anchor="w", fill="x")
        return filters_frame

    def add_info(self):
        title_label = CTkLabel(
            self.frame, text=f"Ranked Open Jobs for: {self.candidate.name} ({self.candidate.candidate_id}). Clearance: {self.candidate.security_clearance}, Location: {self.candidate.location}", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 5), padx=10, anchor="w")

        job_keywords_label = CTkLabel(
            self.frame, text=f"Candidate Resume Keywords: [{', '.join(set(self.candidate.tech_keywords))}].")
        job_keywords_label.pack(pady=(10, 5), padx=10, anchor="w")
