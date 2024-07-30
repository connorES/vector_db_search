from ui.components.results.base_results_table import BaseResultsTable


class QdrantJobResultsTable(BaseResultsTable):
    def __init__(self, master, results, keywords, height=400):
        self.keywords = keywords
        super().__init__(master, results, height)

    def get_selected(self):
        return self.sheet.get_currently_selected()

    def prepare_results(self):
        if not self.results:
            return

        formatted_results = []

        for result in self.results:
            score = round((result[1] * 100), 2)
            payload = result[0].payload
            job_id = result[0].id
            job_title = payload['title']
            clearance = payload['clearance']
            closing_date = payload['closing_date'][:10]
            client = payload['client']
            location = ', '.join(payload['location'])
            manager = payload['manager']
            keywords = ', '.join(set([keyword for keyword in payload['tech_keywords'] if keyword in self.keywords]))

            formatted_results.append(
                [job_id, job_title, client, clearance, location, closing_date, manager, score, keywords])

        self.formatted_results = formatted_results

    def set_headers(self):
        headers = ["Job ID", "Job Title", "Client", "Job Clearance", "Job Location(s)", "Closing Date", "Manager",
                   "Score",  "Matching Keywords"]
        self.sheet.headers(headers)
