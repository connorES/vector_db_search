from customtkinter import CTkFrame, CTkLabel


class ResultsSearchInfoPanel:
    def __init__(self, master, job=None, keywords=None, input_string=None, filters=None):
        self.master = master
        self.job = job
        self.filters = filters
        self.keywords = keywords
        self.input_string = input_string
        self.frame = self.create_frame()
        self.add_info()

    def create_frame(self):
        filters_frame = CTkFrame(master=self.master)
        filters_frame.pack(pady=20, padx=10, anchor="w", fill="x")
        return filters_frame

    def add_info(self):
        if self.job is not None:
            title_label = CTkLabel(
                self.frame, text=f"Search Results for: {self.job.job_title} ({self.job.job_id}). Clearance: {self.job.clearance}, Location(s): {', '.join(self.job.location)}", font=("Arial", 16, "bold"))
            title_label.pack(pady=(10, 5), padx=10, anchor="w")

            job_keywords_label = CTkLabel(
                self.frame, text=f"Job Keywords: [{', '.join(set(self.job.desc_tech_keywords + self.job.title_tech_keywords))}]. Currently Applied Filters: [{', '.join(self.filters) if self.filters else 'None'}]")
            job_keywords_label.pack(pady=(10, 5), padx=10, anchor="w")

        else:
            title_label = CTkLabel(
                self.frame, text=f"Custom Search", font=("Arial", 16, "bold"))
            title_label.pack(pady=(10, 5), padx=5, anchor="w")

            query_text_label = CTkLabel(
                self.frame, text=f"Input: {self.input_string[:100].strip()}...")
            query_text_label.pack(pady=(10, 5), padx=5, anchor="w")

            job_keywords_label = CTkLabel(
                self.frame, text=f"Keywords: [{', '.join(set(self.keywords))}]")
            job_keywords_label.pack(pady=(10, 5), padx=5, anchor="w")