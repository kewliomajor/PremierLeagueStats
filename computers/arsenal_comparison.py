from model import mongo_client, league_table_class, stats_encoder_class, team_results_class
from model.arsenal_comparison_class import ArsenalComparison
from model.previous_season_comparison_class import PreviousSeasonComparison
from model.promotion_mappings import get_promotion_mappings

client = mongo_client.MongoClient()

def compute_comparison(computed_stats, current_team_stats, arsenal_stats):
    same_games_arsenal_points = 0
    same_games_opponent_points = 0
    same_games_played = 0
    different_games_arsenal_points = 0
    different_games_opponent_points = 0
    different_arsenal_games_played = 0
    different_opponent_games_played = 0

    for opponent_fixtures in current_team_stats.fixtures:
        if opponent_fixtures.opponent == "Arsenal":
            if opponent_fixtures.home_points is not None:
                same_games_opponent_points += opponent_fixtures.home_points
                if opponent_fixtures.home_points == 1:
                    same_games_arsenal_points += 1
                else:
                    same_games_arsenal_points += 3 - opponent_fixtures.home_points
                same_games_played += 1
            if opponent_fixtures.away_points is not None:
                same_games_opponent_points += opponent_fixtures.away_points
                if opponent_fixtures.away_points == 1:
                    same_games_arsenal_points += 1
                else:
                    same_games_arsenal_points += 3 - opponent_fixtures.away_points
                same_games_played += 1
            continue
        for arsenal_fixtures in arsenal_stats.fixtures:
            if opponent_fixtures.opponent == arsenal_fixtures.opponent:
                if opponent_fixtures.home_points is not None and arsenal_fixtures.home_points is not None:
                    same_games_arsenal_points += arsenal_fixtures.home_points
                    same_games_opponent_points += opponent_fixtures.home_points
                    same_games_played += 1
                elif opponent_fixtures.home_points is not None and arsenal_fixtures.home_points is None:
                    different_games_opponent_points += opponent_fixtures.home_points
                    different_opponent_games_played += 1
                elif opponent_fixtures.home_points is None and arsenal_fixtures.home_points is not None:
                    different_games_arsenal_points += arsenal_fixtures.home_points
                    different_arsenal_games_played += 1

                if opponent_fixtures.away_points is not None and arsenal_fixtures.away_points is not None:
                    same_games_arsenal_points += arsenal_fixtures.away_points
                    same_games_opponent_points += opponent_fixtures.away_points
                    same_games_played += 1
                elif opponent_fixtures.away_points is not None and arsenal_fixtures.away_points is None:
                    different_games_opponent_points += opponent_fixtures.away_points
                    different_opponent_games_played += 1
                elif opponent_fixtures.away_points is None and arsenal_fixtures.away_points is not None:
                    different_games_arsenal_points += arsenal_fixtures.away_points
                    different_arsenal_games_played += 1


    computed_stats.direct_fixture_games_played = same_games_played
    computed_stats.direct_fixture_percentage_played = same_games_played / 38 * 100
    computed_stats.direct_fixture_points_comparison = same_games_arsenal_points - same_games_opponent_points
    if same_games_played != 0:
        computed_stats.direct_fixture_ppg_comparison = (same_games_arsenal_points/same_games_played) - (same_games_opponent_points/same_games_played)
    computed_stats.points_to_match_arsenal = different_games_arsenal_points
    if different_arsenal_games_played != 0:
        computed_stats.ppg_to_match_arsenal = different_games_arsenal_points/different_arsenal_games_played
    computed_stats.points_for_arsenal_to_match = different_games_opponent_points
    if different_opponent_games_played != 0:
        computed_stats.ppg_for_arsenal_to_match = different_games_opponent_points/different_opponent_games_played

    return computed_stats

def compute_if_team_can_finish_above(computed_stats, current_table, current_team_stats):
    arsenal_points = 0
    arsenal_games_played = 0
    for current_table_row in current_table.standings:
        if current_table_row.team_name == "Arsenal":
            arsenal_points = current_table_row.points
            arsenal_games_played = current_table_row.games_played
            break

    for current_table_row in current_table.standings:
        if current_table_row.team_name == current_team_stats.team_name:
            computed_stats.can_finish_above = (current_table_row.maximum_possible_points >= arsenal_points)
            computed_stats.arsenal_points_to_finish_above = current_table_row.maximum_possible_points - arsenal_points
            computed_stats.arsenal_ppg_to_finish_above = computed_stats.arsenal_points_to_finish_above/(38-arsenal_games_played)
            break
    return computed_stats

def compute_ordered_change(computed_stats, current_team_stats, arsenal_stats):
    current_team_games = len(current_team_stats.ordered_results)
    arsenal_games = len(current_team_stats.ordered_results)
    opponent_points = 0
    arsenal_points = 0

    if current_team_games >= 10 and arsenal_games >= 10:
        for current_results in current_team_stats.ordered_results[:10]:
            opponent_points += current_results.points
        for past_results in arsenal_stats.ordered_results[:10]:
            arsenal_points += past_results.points
        computed_stats.first_10_points_comparison = arsenal_points - opponent_points
        computed_stats.first_10_ppg_comparison = computed_stats.first_10_points_comparison / 10

    if current_team_games >= 20 and arsenal_games >= 20:
        opponent_points = 0
        arsenal_points = 0
        for current_results in current_team_stats.ordered_results[11:20]:
            opponent_points += current_results.points
        for past_results in arsenal_stats.ordered_results[11:20]:
            arsenal_points += past_results.points
        computed_stats.second_10_points_comparison = arsenal_points - opponent_points
        computed_stats.second_10_ppg_comparison = computed_stats.second_10_points_comparison / 10

    if current_team_games >= 30 and arsenal_games >= 30:
        opponent_points = 0
        arsenal_points = 0
        for current_results in current_team_stats.ordered_results[21:30]:
            opponent_points += current_results.points
        for past_results in arsenal_stats.ordered_results[21:30]:
            arsenal_points += past_results.points
        computed_stats.third_10_points_comparison = arsenal_points - opponent_points
        computed_stats.third_10_ppg_comparison = computed_stats.third_10_points_comparison / 10

        opponent_points = 0
        arsenal_points = 0
        current_team_games = len(current_team_stats.ordered_results)
        arsenal_games = len(current_team_stats.ordered_results)
        if current_team_games > arsenal_games:
            max_games = arsenal_games
        else:
            max_games = current_team_games

        for current_results in current_team_stats.ordered_results[30:max_games]:
            opponent_points += current_results.points
        for past_results in arsenal_stats.ordered_results[30:max_games]:
            arsenal_points += past_results.points
        computed_stats.last_8_points_comparison = arsenal_points - opponent_points
        computed_stats.last_8_ppg_comparison = computed_stats.last_8_points_comparison / 10

    return computed_stats

def compute_team_comparison(current_year, current_table, current_team_stats, arsenal_stats):
    stats_doc = client.get_arsenal_season_comparison()
    team_stats_query = {"team_name": current_team_stats.team_name, "season": current_year}
    previous_stats = stats_doc.find_one(team_stats_query)

    if previous_stats:
        computed_stats = ArsenalComparison(**previous_stats)
    else:
        computed_stats = ArsenalComparison()
        computed_stats.team_name = current_team_stats.team_name
        computed_stats.season = current_year

    computed_stats = compute_if_team_can_finish_above(computed_stats, current_table, current_team_stats)
    computed_stats = compute_comparison(computed_stats, current_team_stats, arsenal_stats)
    computed_stats = compute_ordered_change(computed_stats, current_team_stats, arsenal_stats)

    return computed_stats

def compute_arsenal_comparison(current_year):
    table_doc = client.get_league_table_document()
    teams_doc = client.get_team_results_document()

    table_query = {"season": current_year}
    current_table = table_doc.find_one(table_query)
    current_table = league_table_class.LeagueTable.from_mongo(current_table)

    for current_table_row in current_table.standings:
        team_stats_query = {"season": current_year, "team_name": current_table_row.team_name}
        current_team_stats = teams_doc.find_one(team_stats_query)
        current_team_stats = team_results_class.TeamResults.from_mongo(current_team_stats)

        if current_team_stats.team_name == "Arsenal":
            continue

        arsenal_stats_query = {"season": current_year, "team_name": "Arsenal"}
        arsenal_stats = teams_doc.find_one(arsenal_stats_query)
        arsenal_stats = team_results_class.TeamResults.from_mongo(arsenal_stats)

        team_data = compute_team_comparison(current_year, current_table, current_team_stats, arsenal_stats)

        stats_doc = client.get_arsenal_season_comparison()
        stats_doc.replace_one(team_stats_query, stats_encoder_class.to_dict_native(team_data), upsert=True)

    return None