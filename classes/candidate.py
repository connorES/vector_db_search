from copy import deepcopy
from docx2txt import process
from pypdf import PdfReader
from utils.rescource_path import resource_path
from utils.constants import CLASS_TO_STATE


class Candidate:
    def __init__(self, candidate_id):
        self.candidate_id = candidate_id
        self.name = None
        self.resume_keywords = None
        self.current_role = None
        self.security_clearance = None
        self.score = None
        self.keywords_string = None
        self.resume_path = None
        self.last_4_weeks = None
        self.tris_data = None
        self.location = None
        self.bonus_score = None
        self.resume_string = None
        self.state = None
        self.candidate_class = None
        self.update_date = None
        self.tech_keywords = []

    def clone(self):
        new_candidate = deepcopy(self)
        return new_candidate

    def add_text(self):
        file = self.resume_path
        try:
            if file.endswith(".pdf"):
                with open(file, "rb") as f:
                    pdf_reader = PdfReader(f)
                    self.resume_string = "".join(
                        page.extract_text() for page in pdf_reader.pages)
            elif file.endswith(".docx") or file.endswith(".DOCX") or file.endswith(".doc"):
                self.resume_string = process(file)
            else:
                self.resume_string = self.tris_data
        except Exception as e:
            self.resume_string = self.tris_data

    def get_keywords_string(self):
        self.keywords_string = ""
        for tuple in self.resume_keywords:
            self.keywords_string += ", " + tuple[0]
        return self.keywords_string

    def get_email_link(self):
        cand_doc_path = (self.resume_path[58::]).replace("\\", "/")
        resume_link_string = resource_path("redacted") + cand_doc_path
        return resume_link_string

    def get_total_score(self):
        return self.score + float(self.bonus_score or 0)

    def list_attributes(self):
        return [self.name, self.resume_keywords, self.current_role, self.security_clearance, self.score]

    # specify the property to be used when comparing two candidates (eg. if canididate1 == candidate2)
    def __eq__(self, other):
        if isinstance(other, Candidate):
            return self.candidate_id == other.candidate_id

    # similar as above but for sets (eg. if candidate in set_of_candidates)
    def __hash__(self):
        return hash(self.candidate_id)

    def get_short_score(self):
        return round(self.get_total_score() * 100, 1)

    def set_location(self):
        self.location = CLASS_TO_STATE.get(self.candidate_class)

    def set_clearance(self, db_clearance):
        if "-" in db_clearance:
            db_clearance = db_clearance[:db_clearance.index(" ")].strip()
        self.security_clearance = db_clearance

    def get_clearances(self):
        clearances = ["None", "Baseline", "NV1", "NV2", "TSPV"]
        valid_clearances = clearances[:clearances.index(self.clearance)]
        self.valid_clearances = valid_clearances
        return valid_clearances
