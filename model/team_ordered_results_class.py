class TeamOrderedResults:
    def __init__(self, **kwargs):
        # Dynamically set any keys passed from the dictionary, defaulting to None
        self.opponent = kwargs.get("opponent")
        self.points = kwargs.get("points")
        self.goals_for = kwargs.get("goals_for")
        self.goals_against = kwargs.get("goals_against")