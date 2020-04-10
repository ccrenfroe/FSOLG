# Web Scrapper for NBA.com
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# Imports here
import pandas
from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup
from datetime import date

## Maybe keep these
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



# Global variables here
DELAY = 5
TOTAL_NBA_TEAMS = 30
BASE_URL = "https://www.basketball-reference.com"
TEAMS = ['ATL','BOS','BRK','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND', 'LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS'] # Current NBA teams. Abbreviations are according to basketball-reference.com

# Webdriver
driver = webdriver.Chrome() # PLACE DRIVERS EXECUTABLE PATH HERE IN THIS FORM : ("PATH_HERE"). REFER TO THE INSTALLATION GUIDE.

# Input  : None
# Output : Outputs a new CSV for each team and players with basic data.
# Purpose: Makes initial CSVs for every team and player. This is done when the user wants to start fresh. An example case could be if the user wants to start fresh for a new season.
def init_csvs():

    for team in TEAMS:
        #print(team) # Testing output
        # Building up the URL
        current_year = date.today().year
        team_url = BASE_URL + "/teams/" + team + "/" + str(current_year) + ".html"
        print(team_url) # URL of current team
        driver.get(team_url) # Running the webdriver to get to the URL
        soup = BeautifulSoup(driver.page_source,'lxml') # lxml is a little faster, so opt for this instead of html.parser

        # Initializing the team CSVs
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

        # Initializing the player CSVs
        # BeautifulSoup parsing to find the URL resource for each players page
        roster_table = soup.find("table",{"id":"roster"}) # Find the roster table
        rows = roster_table.find("tbody").find_all("td",{"data-stat":"player"}) # Find all of the table rows about the players
        for row in rows: # Go through each row of the table and find the player resource
            link = row.find(href=True)
            #print(link['href']) Testing output
            player_url = BASE_URL + link['href'] # Build the URL for the players webpage
            #print(player_url) Testing output
            driver.get(player_url)
            soup = BeautifulSoup(driver.page_source,'lxml')
            #print(soup)
            info_panel = soup.find("div",{"id":"meta"}) # Focus on the section of the page with all of the basic player info needed
            #print(info_panel) Testing output
            player_name = info_panel.find("h1",{"itemprop":"name"}).text # Get the players name
            #print(player_name) Testing output
            info_panel_rows = info_panel.find_all("p") # Find each row of info in the info_panel section
            #print(info_panel_rows)

            # This section is split up into different cases. The 2 main cases are if the first row is a pronunciation row or not. From there, it is also broken up into if the player had a previous name or not, as well as a nickname. This matters as the differences cascade the rows, causing the indexes to change.
            if (info_panel_rows[0].find("strong").text == "Pronunciation"): # First row is pronunciation
                full_name = info_panel_rows[1].find("strong").find("strong").text # Get the players full name. Useful in case there are players with the same names that need to be distinguished between.
                if(info_panel_rows[2].find("strong") != None): # Executes this path if there is no nickname line for the player
                    position = info_panel_rows[2].find("strong").next_sibling # Get the position. Currently bugged and giving weird output
                    position = str(position).strip()
                    height = info_panel_rows[3].find("span",{"itemprop":"height"}).text # Get height
                    weight = info_panel_rows[3].find("span",{"itemprop":"weight"}).text # Get weight
                else: # Executes this path if the player has nicknames
                    if(info_panel_rows[3].find("strong") != None): # Normal path
                        position = info_panel_rows[3].find("strong").next_sibling
                        position = str(position).strip()
                        height = info_panel_rows[4].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[4].find("span",{"itemprop":"weight"}).text
                    else: # Special path for players with a different birthname and nickname. Ex: Bismack Biyombo
                        position = info_panel_rows[4].find("strong").next_sibling
                        position = str(position).strip()
                        height = info_panel_rows[5].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[5].find("span",{"itemprop":"weight"}).text
                        team = info_panel_rows[6].find("a").text

            else:
                full_name = info_panel_rows[0].find("strong").find("strong").text
                if(info_panel_rows[1].find("strong") != None): # Executes this path if there is no nickname line for the player
                    position = info_panel_rows[1].find("strong").next_sibling
                    position = str(position).strip()
                    height = info_panel_rows[2].find("span",{"itemprop":"height"}).text
                    weight = info_panel_rows[2].find("span",{"itemprop":"weight"}).text
                else: # Executes this path if the player has nicknames
                    if (info_panel_rows[2].find("strong") != None):
                        position = info_panel_rows[2].find("strong").next_sibling
                        position = str(position).strip()
                        height = info_panel_rows[3].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[3].find("span", {"itemprop": "weight"}).text
                    else:  # Special path for players with a different birthname and nickname. Ex: Willie Cauley-Stein
                        position = info_panel_rows[3].find("strong").next_sibling
                        position = str(position).strip()
                        height = info_panel_rows[4].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[4].find("span", {"itemprop": "weight"}).text

                    # Testing output
                    # print(full_name)
                    # print(height)
                    # print(weight)
                    # print(team)
                    # print(position) Skipping position for now due to weird output. Posted a Stack Overflow question

            # Create a CSV to append all od the gathered data to
            with open(player_name + '.csv', 'w', newline='') as f:  # Create a CSV for the current team
                writer = csv.writer(f)  # Create a writer for the csv
                # Write to the CSV all of the gathered data
                writer.writerow(["team",team_name])
                writer.writerow(["full name",full_name])
                writer.writerow(["position"])
                writer.writerow(["height",height])
                writer.writerow(["weight",weight])
    return

# Input: Teams to check injury list for
# Output: New Injuries.csv and updated injury tables for the chosen teams
# Purpose: Used to update the injuries in the Injuries csv and given teams csv's to allow for the user to check who is injured before a game to give them accurate results.
def injury_update():
    return

# Testing
# Running time test
start_time = time.time()
test = init_csvs()
print("Execution time: " + str((time.time() - start_time)))


#TODO
# Scrape any info needed for the teams. Determine this with clients and Colin, taking out what will be unnecessary.
# Scrape player data
# Scrape injuries
# Integrate with a Main terminal program
# Make sure to prompt the user that when they use the init functions, any existing CSVs will be overwritten.