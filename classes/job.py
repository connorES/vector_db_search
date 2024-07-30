from utils.constants import STATES, CITY_TO_STATE, STATE_TO_CLASS


class Job:
    def __init__(self, job_id):
        self.job_id = job_id
        self.keywords = None
        self.manager = None
        self.job_desc = None
        self.job_title = None
        self.client = None
        self.candidates = []
        self.keywords_string = None
        self.top_candidates = None
        self.clearance = None
        self.location = None
        self.closing_date = None
        self.location_codes = []
        self.wide_cands = []
        self.title_tech_keywords = []
        self.desc_tech_keywords = []
        self.linked_candidate_ids = []

    def get_keywords_string(self):
        self.keywords_string = ""
        for tuple in self.keywords:
            self.keywords_string += ", "+tuple[0]
        return self.keywords_string

    def list_attributes(self):
        return [self.job_id, self.job_title, [(cand.name, cand.get_total_score()) for cand in self.sort_candidates_by_score()]]

    def sort_candidates_by_score(self):
        self.candidates = sorted(self.candidates, key=lambda candidate: float(
            '-inf') if candidate.get_total_score() is None else candidate.get_total_score(), reverse=True)
        return self.candidates

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.job_id == other.job_id

    def __hash__(self):
        return hash(self.job_id)

    def get_location_codes(self):
        pass

    def set_clearance(self):
        text = self.job_desc.lower().split()
        if "nv1" in text:
            self.clearance = "NV1"
        elif "nv2" in text:
            self.clearance = "NV2"
        elif "baseline" in text:
            self.clearance = "Baseline"
        elif "tspv" in text:
            self.clearance = "TSPV"
        else:
            self.clearance = "None"

    def set_location(self):
        text = str(self.location).lower()
        job_states = []

        # Find states and cities in the job description
        for state in STATES:
            if state.lower() in text:
                job_states.append(state)
        for city, state in CITY_TO_STATE.items():
            if city.lower() in text:
                job_states.append(state)
        self.location = list(set(job_states))
        self.location_codes = [
            code for state in job_states for code in STATE_TO_CLASS[state]]

    # def get_wide_search_cands(self):
    #     self.wide_cands = wide_search(self)

    def get_clearances(self):
        clearances = ["None", "Baseline", "NV1", "NV2", "TSPV"]
        valid_clearances = clearances[clearances.index(self.clearance):]
        self.valid_clearances = valid_clearances
        return valid_clearances
