class TeamFixtures:
    def __init__(self, **kwargs):
        # Dynamically set any keys passed from the dictionary, defaulting to None
        self.opponent = kwargs.get("opponent")
        self.home_points = kwargs.get("home_points")
        self.home_goals_for = kwargs.get("home_goals_for")
        self.home_goals_against = kwargs.get("home_goals_against")
        self.away_points = kwargs.get("away_points")
        self.away_goals_for = kwargs.get("away_goals_for")
        self.away_goals_against = kwargs.get("away_goals_against")