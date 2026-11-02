from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from model import mongo_client, league_table_row_class, league_table_class, stats_encoder_class, scraper_index_constants
import json


def update_table(url, year, current_year = True):
    print_only = False
    client = mongo_client.MongoClient()
    table_doc = client.get_league_table_document()

    query = {"season": year}
    existing_table = table_doc.find_one(query)
    existing_table = league_table_class.LeagueTable.from_mongo(existing_table)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headful often passes easier
        context = browser.new_context(storage_state="browser-state.json")
        page = context.new_page()

        # Hide automation flags
        stealth_sync(page)

        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)  # Give time for the challenge to finish

        soup = BeautifulSoup(page.content(), "html.parser")

        center_page = soup.find("div",
                                style="width:700px;margin-left:28px;padding-left:4px;margin-right:0px;margin-top:3px;float:left;")

        tables = center_page.find_all("table", id="btable")

        fixed_index_table = scraper_index_constants.get_fixed_index_table(current_year)
        league_table_html = tables[fixed_index_table[0]]

        rows = league_table_html.find_all("tr", class_="odd")

        if existing_table is None:
            league_table = league_table_class.LeagueTable()
        else:
            league_table = existing_table
            league_table.standings = []

        league_table.season = year

        for row in rows:
            columns = row.find_all("td")
            num_columns = len(columns)
            variable_indicies = scraper_index_constants.get_variable_index_table(num_columns, current_year)
            webpage_row = league_table_row_class.LeagueTableRow()
            webpage_row.link = columns[fixed_index_table[1]].find("a")["href"]
            webpage_row.position = int(columns[fixed_index_table[2]].text.strip())
            webpage_row.team_name = columns[fixed_index_table[3]].text.strip()
            webpage_row.games_played = int(columns[fixed_index_table[4]].text.strip())
            webpage_row.wins = int(columns[fixed_index_table[5]].text.strip())
            webpage_row.draws = int(columns[fixed_index_table[6]].text.strip())
            webpage_row.losses = int(columns[fixed_index_table[7]].text.strip())
            webpage_row.goals_for = int(columns[fixed_index_table[8]].text.strip())
            webpage_row.goals_against = int(columns[fixed_index_table[9]].text.strip())
            webpage_row.goal_differential = int(columns[fixed_index_table[10]].text.strip())
            webpage_row.points = int(columns[fixed_index_table[11]].text.strip())
            webpage_row.points_per_game = float(columns[variable_indicies[0]].text.strip())
            webpage_row.last_8 = float(columns[variable_indicies[1]].text.strip())
            webpage_row.clean_sheet_percentage = int(columns[variable_indicies[2]].text.strip().rstrip("%"))
            webpage_row.score_rate_percentage = int(columns[variable_indicies[3]].text.strip().rstrip("%"))
            if current_year:
                webpage_row.maximum_possible_points = int(columns[variable_indicies[4]].text.strip())

            league_table.standings.append(webpage_row)

        if not print_only:
            table_doc.replace_one(query, stats_encoder_class.to_dict_native(league_table), upsert=True)
        else:
            print(json.dumps(league_table, cls=stats_encoder_class.StatsEncoder))