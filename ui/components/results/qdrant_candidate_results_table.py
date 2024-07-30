from ui.components.results.base_results_table import BaseResultsTable
from os import startfile
from os import path


class QdrantCandidateResultsTable(BaseResultsTable):
    def __init__(self, master, results, keywords, height=600):
        self.keywords = keywords
        self.resume_paths = []
        super().__init__(master, results, height)
        self.sheet.extra_bindings("begin_edit_cell", self.open_document)

    def get_selected(self):
        return self.sheet.get_currently_selected()

    def prepare_results(self):
        if not self.results:
            self.formatted_results = []
            return
        
        formatted_results = []
        resume_paths = []
        
        for result in self.results:
            score = round((result[1] * 100), 2)
            payload = result[0].payload

            cand_class = int(payload['class'])
            cand_id = result[0].id
            clearance = payload['clearance']
            location = payload['location']
            try:
                name = payload['name']
            except KeyError:
                name = "Name not found"

            try:
                resume_path = payload['path']
            except KeyError:
                resume_path = "Path not found"

            try:
                current_role = payload['current_role']
            except KeyError:
                current_role = "Role not found"

            try:
                last_updated = str(payload['last_updated'])[:7]
            except KeyError:
                last_updated = "Date not found"

            try:
                matching_keywords = ', '.join([
                    keyword for keyword in payload['tech_keywords'] if keyword in self.keywords])
            except KeyError:
                matching_keywords = []

            formatted_results.append(
                    [cand_id, name, current_role, cand_class, score, clearance, location, last_updated, matching_keywords])
            resume_paths.append(resume_path)
            self.formatted_results = formatted_results
            self.associated_data['resume_paths'] = resume_paths


    def set_headers(self):
        headers = ["ID", "Name", "Current Role", "Class",
                   "Score", "Clearance", "Location", "CV Updated", "Matching Keywords"]
        self.sheet.headers(headers)


    def open_document(self, event):
        row = event.row
        file_path = self.associated_data['resume_paths'][row]  # Use associated_data
        if path.isfile(file_path):
            startfile(file_path)
        else:
            print(f"File not found: {file_path}")
