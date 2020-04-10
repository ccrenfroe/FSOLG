# Web Scrapper for NBA.com
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# Imports here
import pandas
from selenium import webdriver

## Maybe keep these
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import csv
from bs4 import BeautifulSoup
from datetime import date

# Global variables here
DELAY = 5
TOTAL_NBA_TEAMS = 30
TEAM_URL = "https://www.basketball-reference.com/teams/"
TEAMS = ['ATL','BOS','BRK','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND', 'LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS'] # Current NBA teams. Abbreviations are according to basketball-reference.com

# Webdriver
driver = webdriver.Chrome() # PLACE DRIVERS EXECUTABLE PATH HERE


# Input :
# Output : Outputs a new CSV for each team with basic data.
# Purpose: Makes initial CSVs for everyteam. This is done when the user wants to start fresh. An example case could be if the user wants to start fresh for a new season.
def init_teams():

    for team in TEAMS:
        print(team) # Testing
        # Building up the URL
        current_year = date.today().year
        team_url = TEAM_URL + team + "/" + str(current_year) + ".html"
        print(team_url) # URL of current team
        driver.get(team_url) # Running the webdriver to get to the URL
        soup = BeautifulSoup(driver.page_source,'lxml') # lxml is a little faster, so opt for this instead of html.parser

        # BeautifulSoup parsing to find the URL resource for each players page
        roster_table = soup.find("table",{"id":"roster"})
        rows = roster_table.find("tbody").find_all("td",{"data-stat":"player"})
        player_pages = [] # List of the player resources
        for row in rows: # Go through each row of the table and find the player resource to append to the player_pages list
            link = row.find(href=True)
            player_pages.append(link)

        team_name = soup.find("h1",{"itemprop":"name"}).find_all("span")[1].text # BeauitfulSoup parsing to find the team name
        df = pandas.read_html(driver.page_source) # Returns all of the tables on the webpage
        team_roster= df[0].loc[:,"Player"] # Take the first table, the roster
        #print(team_roster) # Testing
        if ("Description" in df[1].columns): # If the table has a description column, that means its the injury table
            injuries = df[1].loc[:,"Player"]
            #print(injuries) # Testing

        # Create a CSV to append all od the gathered data to
        with open(team_name + '.csv', 'w', newline='') as f: # Create a CSV for the current team
            writer = csv.writer(f) # Create a writer for the csv
            writer.writerow(["Roster"]) # Teams roster
            for player in team_roster: # Add each player
                writer.writerow([player])
            writer.writerow(["Injuries"]) # Teams current injuries
            for player in injuries: # Add each injured player
                writer.writerow([player])
    return

def injury_update():
    return

# Testing
# Running time test
start_time = time.time()
test = init_teams()
print("Execution time: " + str((time.time() - start_time)))


#TODO
# Scrape any info needed for the teams
# Create player_init
# Scrape player data
# Scrape injuries
# Integrate with a Main terminal program
# Make sure to prompt the user that when they use the init functions, any existing CSVs will be overwritten.