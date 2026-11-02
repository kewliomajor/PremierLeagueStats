from computers import previous_season_comparision, arsenal_comparison

current_year = 2027


def compute_custom_stats():
    previous_season_comparision.compute_previous_season_comparison(current_year)
    arsenal_comparison.compute_arsenal_comparison(current_year)