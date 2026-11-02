class PreviousSeasonComparison:
    def __init__(self, **kwargs):
        # Dynamically set any keys passed from the dictionary, defaulting to None
        if kwargs.get("_id") is not None:
            self._id = kwargs.get("_id")
        self.team_name = kwargs.get("team_name")
        self.season = kwargs.get("season")
        self.points_change = kwargs.get("points_change")
        self.ppg_change = kwargs.get("ppg_change")
        self.projected_points = kwargs.get("projected_points")
        self.projected_ppg = kwargs.get("projected_ppg")
        self.ordered_points_change = kwargs.get("ordered_points_change")
        self.ordered_ppg_change = kwargs.get("ordered_ppg_change")
        self.first_10_change = kwargs.get("first_10_change")
        self.first_10_ppg_change = kwargs.get("first_10_ppg_change")
        self.second_10_change = kwargs.get("second_10_change")
        self.second_10_ppg_change = kwargs.get("second_10_ppg_change")
        self.third_10_change = kwargs.get("third_10_change")
        self.third_10_ppg_change = kwargs.get("third_10_ppg_change")
        self.last_8_change = kwargs.get("last_8_change")
        self.last_8_ppg_change = kwargs.get("last_8_ppg_change")