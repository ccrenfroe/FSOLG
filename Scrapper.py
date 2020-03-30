# Web Scrapper for NBA.com
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# Imports here
from typing import Dict, List, Any
import requests
import csv

# Global variables here
KEY = "4b366503c3msh01406076be9e83cp1f4e6fjsn4bade6c668b7" # IMPORTANT: Change this to the unique key attached to your account for API-NBA. (https://rapidapi.com/api-sports/api/api-nba/endpoints)
TOTAL_NBA_TEAMS = 30

teams_url = "https://api-nba-v1.p.rapidapi.com/teams/confName/"
conferences = ["East","West"] # This makes it easier to get the data needed and doesn't return the foreign teams also included in the whole "teams/standard" request response. Narrows it down to only US teams.

# Host and unique key to access the API
headers = {
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
    'x-rapidapi-key': KEY
    }

# Input : Takes in the urls for the API and then a conference list that has the extra parameter for the URL, the East and West conference of the NBA.
# Output : Outputs a new CSV for each team with basic data.
# Purpose: Makes initial CSVs for everyteam. This is done when the user wants to start fresh. An example case could be if the user wants to start fresh for a new season.
def init_teams(teams_url, conferences):
    i = 0
    while (i < 2):
        # Send request to the API and receive the response back
        response = requests.request("GET", teams_url + conferences[i], headers=headers)
        response = response.json()
        teams = response["api"]["teams"] # Get rid of the unnecessary part of the response. Cleans it down to the list of teams.
        # Go through the list of teams and create a new CSV for each team.
        for team in teams:
            teamName = team["nickname"]
            # Skip these. These aren't actual NBA teams, but rather teams for special events. Could be changed to be included if the Client desires so.
            if((teamName == "Team Giannis") or (teamName == "Team Wilbon") or (teamName == "Team Stephen A") or (teamName == "USA") or (teamName == "World") or (teamName == "Team Giannis") or (teamName == "Team LeBron")):
                continue
            # Creates a new CSV
            ## IMPORTANT NOTE: This will overwrite any existing CSV with the same name.
            with open(teamName + '.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["teamId", team["teamId"]])
                writer.writerow(["city", team["city"]])
                writer.writerow(["fullName", team["fullName"]])
                writer.writerow(["nickname", team["nickname"]])
                writer.writerow(["shortName", team["shortName"]])
        i = i + 1
    return

#Testing shit.
test = init_teams(teams_url,conferences)

#TODO
# Scrape any info needed for the teams
# Create player_init
# Scrape player data
# Integrate with a Main terminal program
# a. Make sure to prompt the user that when they use the init functions, any existing CSVs will be overwritten.