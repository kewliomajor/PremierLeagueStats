import pymongo


class MongoClient:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def get_league_table_document(self):
        cs_matches_db = self.client["premier_league_stats"]
        return cs_matches_db["league_table"]

    def get_team_results_document(self):
        cs_matches_db = self.client["premier_league_stats"]
        return cs_matches_db["team_results"]

    def get_previous_season_comparison(self):
        cs_matches_db = self.client["premier_league_stats"]
        return cs_matches_db["previous_season_comparison"]

    def get_arsenal_season_comparison(self):
        cs_matches_db = self.client["premier_league_stats"]
        return cs_matches_db["arsenal_comparison"]
