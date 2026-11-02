import time

from bson import ObjectId

from model.team_fixtures_class import TeamFixtures
from model.team_ordered_results_class import TeamOrderedResults


class TeamResults:
    def __init__(self, _id: ObjectId = None, team_name = None, fetched_at = None, season = None, fixtures : list[TeamFixtures] = [], ordered_results : list[TeamOrderedResults] = []):
        if _id is not None:
            self._id = _id
        self.team_name = team_name
        self.fetched_at = time.time()
        self.season = season
        self.fixtures = fixtures
        self.ordered_results = ordered_results

    @classmethod
    def from_mongo(cls, data):
        if not data:
            return None

        # Deep copy data or work on a shallow copy so we don't mutate the original dict
        data_copy = data.copy()

        if "fixtures" in data_copy and isinstance(data_copy["fixtures"], list):
            data_copy["fixtures"] = [
                TeamFixtures(**row) for row in data_copy["fixtures"]
            ]

        if "ordered_results" in data_copy and isinstance(data_copy["ordered_results"], list):
            data_copy["ordered_results"] = [
                TeamOrderedResults(**row) for row in data_copy["ordered_results"]
            ]

        return cls(**data_copy)
