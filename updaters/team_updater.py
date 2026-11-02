import time

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from model import mongo_client, league_table_class, stats_encoder_class, team_results_class
import json

from model.team_fixtures_class import TeamFixtures
from model.team_ordered_results_class import TeamOrderedResults


def update_fixtures(team_results, soup):
    right_page = soup.find("div",
                           style="width:297px;margin-left:28px;float:left;")

    if right_page is None:
        print("Right page panel doesn't exist")
        exit()

    tables_html = right_page.find_all("table", id="btable")
    rows = tables_html[0].find_all("tr", class_="odd")

    for row in rows:
        columns = row.find_all("td")
        # this row has the current team (no home/away data)
        if len(columns) == 5:
            continue

        team_fixture = TeamFixtures()
        team_fixture.opponent = columns[1].text.strip()
        home_text = columns[4].text
        away_text = columns[5].text

        if ":" in home_text:
            home_score = home_text.split(":")
            team_fixture.home_goals_for = int(home_score[0])
            team_fixture.home_goals_against = int(home_score[1])
            if team_fixture.home_goals_for > team_fixture.home_goals_against:
                team_fixture.home_points = 3
            elif team_fixture.home_goals_for == team_fixture.home_goals_against:
                team_fixture.home_points = 1
            else:
                team_fixture.home_points = 0
        if ":" in away_text:
            away_score = away_text.split(":")
            team_fixture.away_goals_for = int(away_score[1])
            team_fixture.away_goals_against = int(away_score[0])
            if team_fixture.away_goals_for > team_fixture.away_goals_against:
                team_fixture.away_points = 3
            elif team_fixture.away_goals_for == team_fixture.away_goals_against:
                team_fixture.away_points = 1
            else:
                team_fixture.away_points = 0

        team_results.fixtures.append(team_fixture)

    return team_results

def update_ordered_results(team_results, soup, current_year):
    center_page = soup.find("div",
                           style="width:642px;margin-left:4px;margin-right:3px;float:left;")

    if center_page is None:
        print("Center page panel doesn't exist")
        exit()

    tables = center_page.find_all("table")
    if current_year:
        rows = tables[10].find_all("tr", height="38")
    else:
        rows = tables[4].find_all("tr", height="38")

    for row in rows:
        columns = row.find_all("td")
        ordered_result = TeamOrderedResults()
        home_team = columns[1].text.strip()
        score_text = columns[2].text.strip()[:3]
        score_text = score_text.split(":")
        away_team = columns[3].text.strip()

        if home_team == team_results.team_name:
            ordered_result.opponent = away_team
            ordered_result.goals_for = int(score_text[0])
            ordered_result.goals_against = int(score_text[1])
        else:
            ordered_result.opponent = home_team
            ordered_result.goals_for = int(score_text[1])
            ordered_result.goals_against = int(score_text[0])

        if ordered_result.goals_for > ordered_result.goals_against:
            ordered_result.points = 3
        elif ordered_result.goals_for == ordered_result.goals_against:
            ordered_result.points = 1
        else:
            ordered_result.points = 0
        team_results.ordered_results.append(ordered_result)

    return team_results

def update_teams(base_url, year, skip_existing=False, current_year=True):
    print_only = False
    client = mongo_client.MongoClient()
    table_doc = client.get_league_table_document()
    teams_results_doc = client.get_team_results_document()

    season_query = {"season": year}
    existing_table = table_doc.find_one(season_query)
    existing_table = league_table_class.LeagueTable.from_mongo(existing_table)

    if existing_table is None:
        print("Can't get individual team results if table is not populated")
        exit()

    for team in existing_table.standings:
        team_url = base_url + "/" + team.link

        #prevent rate limiting
        time.sleep(5)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Headful often passes easier
            context = browser.new_context(storage_state="browser-state.json")
            page = context.new_page()

            # Hide automation flags
            stealth_sync(page)

            page.goto(team_url, wait_until="domcontentloaded")
            page.wait_for_timeout(1000)  # Give time for the challenge to finish

            soup = BeautifulSoup(page.content(), "html.parser")

            results_query = {"season": year, "team_name": team.team_name}
            existing_results = teams_results_doc.find_one(results_query)
            existing_results = team_results_class.TeamResults.from_mongo(existing_results)

            if skip_existing and existing_results is not None:
                continue

            if existing_results is None:
                team_results = team_results_class.TeamResults()
                team_results.team_name = team.team_name
                team_results.season = year
            else:
                team_results = existing_results

            team_results.fixtures = []
            team_results.ordered_results = []
            team_results = update_fixtures(team_results, soup)
            team_results = update_ordered_results(team_results, soup, current_year)

            if not print_only:
                teams_results_doc.replace_one(results_query, stats_encoder_class.to_dict_native(team_results), upsert=True)
            else:
                print(json.dumps(team_results, cls=stats_encoder_class.StatsEncoder))

        #context.storage_state(path="browser-state.json")
        #browser.close()