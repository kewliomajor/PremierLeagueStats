from model import mongo_client, league_table_class, stats_encoder_class, team_results_class
from model.previous_season_comparison_class import PreviousSeasonComparison
from model.promotion_mappings import get_promotion_mappings

client = mongo_client.MongoClient()

def compute_points_and_ppg_change(computed_stats, current_year, current_team_stats, previous_team_stats):
    total_points_diff = 0
    total_points_current = 0
    total_points_previous = 0
    total_games = 0

    current_promotion_mappings = get_promotion_mappings()[current_year]

    for current_fixtures in current_team_stats.fixtures:
        for previous_fixtures in previous_team_stats.fixtures:
            if current_fixtures.opponent == previous_fixtures.opponent:
                if current_fixtures.home_points is not None and previous_fixtures.home_points is not None:
                    total_games += 1
                    total_points_diff += current_fixtures.home_points - previous_fixtures.home_points
                    total_points_current += current_fixtures.home_points
                    total_points_previous += previous_fixtures.home_points
                if current_fixtures.away_points is not None and previous_fixtures.home_points is not None:
                    total_games += 1
                    total_points_diff += current_fixtures.away_points - previous_fixtures.away_points
                    total_points_current += current_fixtures.away_points
                    total_points_previous += previous_fixtures.away_points
            elif current_fixtures.opponent in current_promotion_mappings and current_promotion_mappings[
                current_fixtures.opponent] == previous_fixtures.opponent:
                if current_fixtures.home_points is not None and previous_fixtures.home_points is not None:
                    total_games += 1
                    total_points_diff += current_fixtures.home_points - previous_fixtures.home_points
                    total_points_current += current_fixtures.home_points
                    total_points_previous += previous_fixtures.home_points
                if current_fixtures.away_points is not None and previous_fixtures.home_points is not None:
                    total_games += 1
                    total_points_diff += current_fixtures.away_points - previous_fixtures.away_points
                    total_points_current += current_fixtures.away_points
                    total_points_previous += previous_fixtures.away_points

    computed_stats.points_change = total_points_diff
    current_ppg = total_points_current / total_games
    previous_ppg = total_points_previous / total_games
    computed_stats.ppg_change = current_ppg - previous_ppg

    return computed_stats

def compute_projections(computed_stats, current_year, current_team_stats, previous_team_stats):
    current_points = 0
    projected_previous_points = 0
    total_games = 0

    current_promotion_mappings = get_promotion_mappings()[current_year]

    for current_fixtures in current_team_stats.fixtures:
        for previous_fixtures in previous_team_stats.fixtures:
            if current_fixtures.opponent == previous_fixtures.opponent:
                if current_fixtures.home_points is not None:
                    total_games += 1
                    current_points += current_fixtures.home_points
                else:
                    projected_previous_points += previous_fixtures.home_points

                if current_fixtures.away_points is not None:
                    total_games += 1
                    current_points += current_fixtures.away_points
                else:
                    projected_previous_points += previous_fixtures.away_points
            elif current_fixtures.opponent in current_promotion_mappings and current_promotion_mappings[
                current_fixtures.opponent] == previous_fixtures.opponent:
                if current_fixtures.home_points is not None:
                    total_games += 1
                    current_points += current_fixtures.home_points
                else:
                    projected_previous_points += previous_fixtures.home_points

                if current_fixtures.away_points is not None:
                    total_games += 1
                    current_points += current_fixtures.away_points
                else:
                    projected_previous_points += previous_fixtures.away_points

    computed_stats.projected_points = current_points + projected_previous_points
    computed_stats.projected_ppg = projected_previous_points/(38-total_games)

    return computed_stats

def compute_ordered_results_change(computed_stats, current_team_stats, previous_team_stats):
    current_points = 0
    previous_points = 0

    num_games_played = len(current_team_stats.ordered_results)
    for current_results in current_team_stats.ordered_results:
        current_points += current_results.points
    for past_results in previous_team_stats.ordered_results[:num_games_played]:
        previous_points += past_results.points

    computed_stats.ordered_points_change = current_points - previous_points
    computed_stats.ordered_ppg_change = computed_stats.ordered_points_change/num_games_played

    if len(current_team_stats.ordered_results) >= 10:
        current_points = 0
        previous_points = 0
        for current_results in current_team_stats.ordered_results[:10]:
            current_points += current_results.points
        for past_results in previous_team_stats.ordered_results[:10]:
            previous_points += past_results.points
        computed_stats.first_10_change = current_points - previous_points
        computed_stats.first_10_ppg_change = computed_stats.first_10_change/10

    if len(current_team_stats.ordered_results) >= 20:
        current_points = 0
        previous_points = 0
        for current_results in current_team_stats.ordered_results[11:20]:
            current_points += current_results.points
        for past_results in previous_team_stats.ordered_results[11:20]:
            previous_points += past_results.points
        computed_stats.second_10_change = current_points - previous_points
        computed_stats.second_10_ppg_change = computed_stats.second_10_change/10

    if len(current_team_stats.ordered_results) >= 30:
        current_points = 0
        previous_points = 0
        for current_results in current_team_stats.ordered_results[21:30]:
            current_points += current_results.points
        for past_results in previous_team_stats.ordered_results[21:30]:
            previous_points += past_results.points
        computed_stats.third_10_change = current_points - previous_points
        computed_stats.third_10_ppg_change = computed_stats.third_10_change/10

        current_points = 0
        previous_points = 0
        num_games_played = len(current_team_stats.ordered_results)
        for current_results in current_team_stats.ordered_results[30:num_games_played]:
            current_points += current_results.points
        for past_results in previous_team_stats.ordered_results[30:num_games_played]:
            previous_points += past_results.points
        computed_stats.last_8_change = current_points - previous_points
        computed_stats.last_8_ppg_change = computed_stats.last_8_change / 10

    return computed_stats

def compute_team_comparison(current_year, current_team_stats, previous_team_stats):
    stats_doc = client.get_previous_season_comparison()
    team_stats_query = {"team_name": current_team_stats.team_name, "season": current_year}
    previous_stats = stats_doc.find_one(team_stats_query)

    if previous_stats:
        computed_stats = PreviousSeasonComparison(**previous_stats)
    else:
        computed_stats = PreviousSeasonComparison()
        computed_stats.team_name = current_team_stats.team_name
        computed_stats.season = current_year

    computed_stats = compute_points_and_ppg_change(computed_stats, current_year, current_team_stats, previous_team_stats)
    computed_stats = compute_projections(computed_stats, current_year, current_team_stats, previous_team_stats)
    computed_stats = compute_ordered_results_change(computed_stats, current_team_stats, previous_team_stats)

    return computed_stats

def compute_previous_season_comparison(current_year):
    table_doc = client.get_league_table_document()
    teams_doc = client.get_team_results_document()

    table_query = {"season": current_year}
    current_table = table_doc.find_one(table_query)
    current_table = league_table_class.LeagueTable.from_mongo(current_table)

    for current_table_row in current_table.standings:
        team_stats_query = {"season": current_year, "team_name": current_table_row.team_name}
        current_team_stats = teams_doc.find_one(team_stats_query)
        current_team_stats = team_results_class.TeamResults.from_mongo(current_team_stats)

        previous_team_stats_query = {"season": current_year-1, "team_name": current_table_row.team_name}
        previous_team_stats = teams_doc.find_one(previous_team_stats_query)
        previous_team_stats = team_results_class.TeamResults.from_mongo(previous_team_stats)

        if previous_team_stats is None:
            continue

        team_data = compute_team_comparison(current_year, current_team_stats, previous_team_stats)

        stats_doc = client.get_previous_season_comparison()
        stats_doc.replace_one(team_stats_query, stats_encoder_class.to_dict_native(team_data), upsert=True)

    return None