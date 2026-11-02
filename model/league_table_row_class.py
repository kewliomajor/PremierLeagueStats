class LeagueTableRow:
    def __init__(self, **kwargs):
        # Dynamically set any keys passed from the dictionary, defaulting to None
        self.link = kwargs.get("link")
        self.position = kwargs.get("position")
        self.team_name = kwargs.get("team_name")
        self.games_played = kwargs.get("games_played")
        self.wins = kwargs.get("wins")
        self.draws = kwargs.get("draws")
        self.losses = kwargs.get("losses")
        self.goals_for = kwargs.get("goals_for")
        self.goals_against = kwargs.get("goals_against")
        self.goal_differential = kwargs.get("goal_differential")
        self.points = kwargs.get("points")
        self.points_per_game = kwargs.get("points_per_game")
        self.last_8 = kwargs.get("last_8")
        self.clean_sheet_percentage = kwargs.get("clean_sheet_percentage")
        self.score_rate_percentage = kwargs.get("score_rate_percentage")
        self.maximum_possible_points = kwargs.get("maximum_possible_points")

    def get_position(self):
        return self.position

    def get_team_name(self):
        return self.team_name

    def get_games_played(self):
        return self.games_played

    def get_wins(self):
        return self.wins

    def get_draws(self):
        return self.draws

    def get_losses(self):
        return self.losses

    def get_goals_for(self):
        return self.goals_for

    def get_goals_against(self):
        return self.goals_against

    def get_goal_differential(self):
        return self.goal_differential

    def get_points(self):
        return self.points

    def get_points_per_game(self):
        return self.points_per_game

    def get_last_8(self):
        return self.last_8

    def get_clean_sheet_percentage(self):
        return self.clean_sheet_percentage

    def get_score_rate_percentage(self):
        return self.score_rate_percentage

    def get_maximum_possible_points(self):
        return self.maximum_possible_points