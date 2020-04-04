# Web Scrapper for NBA.com
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# Imports here
import requests
import pandas
import selenium
import csv

# Global variables here
TOTAL_NBA_TEAMS = 30
TEAM_URLS = "https://www.basketball-reference.com/teams/"
# Host and unique key to access the API

# Input :
# Output : Outputs a new CSV for each team with basic data.
# Purpose: Makes initial CSVs for everyteam. This is done when the user wants to start fresh. An example case could be if the user wants to start fresh for a new season.
def init_teams():
    response = pandas.read_html(TEAM_URLS)
    r2 = pandas.read_html("https://www.basketball-reference.com/teams/BOS/")
    # response = requests.request("GET",TODAY_URL)
    # response = response.json()response = requests.request("GET",TODAY_URL)
    #response = response.json()
    print(response[0])
    # print(response)
    r2[0]
    #teams = response[]
    return

#
#     conferences = ["East","West"]  # This makes it easier to get the data needed and doesn't return the foreign teams also included in the whole "teams/standard" request response. Narrows it down to only US teams.
#201566
#     i = 0
#     while (i < 2):
#         # Send request to the API and receive the response back
#         response = requests.request("GET", teams_url + conferences[i], headers=headers)
#         response = response.json()
#         teams = response["api"]["teams"] # Get rid of the unnecessary part of the response. Cleans it down to the list of teams.
#         # Go through the list of teams and create a new CSV for each team.
#         for team in teams:
#             teamName = team["nickname"]
#             # Skip these. These aren't actual NBA teams, but rather teams for special events. Could be changed to be included if the Client desires so.
#             if((teamName == "Team Giannis") or (teamName == "Team Wilbon") or (teamName == "Team Stephen A") or (teamName == "USA") or (teamName == "World") or (teamName == "Team Giannis") or (teamName == "Team LeBron")):
#                 continue
#             # Creates a new CSV
#             ## IMPORTANT NOTE: This will overwrite any existing CSV with the same name.
#             with open(teamName + '.csv', 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(["teamId", team["teamId"]])
#                 writer.writerow(["city", team["city"]])
#                 writer.writerow(["fullName", team["fullName"]])
#                 writer.writerow(["nickname", team["nickname"]])
#                 writer.writerow(["shortName", team["shortName"]])
#
#                 response = requests.request("GET", players_url + team["teamId"], headers=headers)
#                 response = response.json()
#                 players = response["api"]["players"]
#
#                 writer.writerow(['Roster'])
#                 for player in players:
#                     print(player)
#                     leagues = player['leagues']
#                     standard = leagues.get('standard', '')
#                     if ((player['startNba'] == '') or (standard == '')):
#                         continue
#                     else:
#                         print("ENTERED THE LOOP")
#                         print(standard)
#                         if (standard['active'] == str(1)):
#                             writer.writerow([player['firstName'] + " " + player['lastName'],player['playerId']])
#                             print("Added player")
#                     #    writer.writerow([player['firstName'] + player['lastName'],player['playerId']])
#                         #print(player)
#
#                 # Invalid if years pro i s 0 startNBA is 0 and active is 0
#
#
#         i = i + 1
#     return

#Testing shit.
test = init_teams()
#TODO
# Scrape any info needed for the teams
# Create player_init
# Scrape player data
# Integrate with a Main terminal program
# a. Make sure to prompt the user that when they use the init functions, any existing CSVs will be overwritten.