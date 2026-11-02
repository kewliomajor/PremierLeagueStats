from compute_custom_stats import compute_custom_stats
from updaters import table_updater, team_updater

base_url = "https://www.soccerstats.com"

url = base_url + "/latest.asp?league=england"

#table_updater.update_table(url, 2027, True)
team_updater.update_teams(base_url, 2027, False, True)

url = url + "_2026"

#only have to run once since it won't change
#table_updater.update_table(url, 2026, False)
#team_updater.update_teams(base_url, 2026, False, False)

compute_custom_stats()
