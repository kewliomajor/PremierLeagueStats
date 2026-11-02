import time

from bson import ObjectId

from model.league_table_row_class import LeagueTableRow


class LeagueTable:
    def __init__(self, _id: ObjectId = None, fetched_at = None, season = None, standings : list[LeagueTableRow] = []):
        if _id is not None:
            self._id = _id
        self.fetched_at = time.time()
        self.season = season
        self.standings = standings

    def get_standings(self):
        return self.standings

    @classmethod
    def from_mongo(cls, data):
        if not data:
            return None

        # Deep copy data or work on a shallow copy so we don't mutate the original dict
        data_copy = data.copy()

        # Map the nested list of dictionaries to LeagueTableRow objects
        if "standings" in data_copy and isinstance(data_copy["standings"], list):
            data_copy["standings"] = [
                LeagueTableRow(**row) for row in data_copy["standings"]
            ]

        return cls(**data_copy)