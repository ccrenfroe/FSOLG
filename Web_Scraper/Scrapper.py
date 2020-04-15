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
import os
from pathlib import Path

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
PROGRAM_ROOT = str(Path(__file__).resolve().parent.parent)


# Webdriver
driver = webdriver.Chrome() # PLACE DRIVERS EXECUTABLE PATH HERE IN THIS FORM : ("PATH_HERE"). REFER TO THE INSTALLATION GUIDE.

def directory_builder():
    if (os.path.isdir(PROGRAM_ROOT + "/Data") == False):
        os.makedirs(PROGRAM_ROOT + '/Data/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Teams/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Players/')
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'), (PROGRAM_ROOT + '/Data/Basketball/Players'))
    else: # Data directory exists
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams'), (PROGRAM_ROOT + '/Data/Basketball/Players'))

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
        with open(os.path.join(TEAMS_DIRECTORY, (team_name + '.csv')), 'w', newline='') as f: # Create a CSV for the current team
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
            letter = link['href'].split("/")[2]
            player_id = link['href'].split("/")[3].split(".")
            player_id = "/" + letter + "/" + player_id[0] + "/"
            print(player_id)
            #print(player_id) Testing output
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
                    height = info_panel_rows[3].find("span",{"itemprop":"height"}).text # Get height
                    weight = info_panel_rows[3].find("span",{"itemprop":"weight"}).text # Get weight
                else: # Executes this path if the player has nicknames
                    if(info_panel_rows[3].find("strong") != None): # Normal path
                        position = info_panel_rows[3].find("strong").next_sibling
                        height = info_panel_rows[4].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[4].find("span",{"itemprop":"weight"}).text
                    else: # Special path for players with a different birthname and nickname. Ex: Bismack Biyombo
                        position = info_panel_rows[4].find("strong").next_sibling
                        height = info_panel_rows[5].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[5].find("span",{"itemprop":"weight"}).text

            else:
                full_name = info_panel_rows[0].find("strong").find("strong").text
                if(info_panel_rows[1].find("strong") != None): # Executes this path if there is no nickname line for the player
                    position = info_panel_rows[1].find("strong").next_sibling
                    height = info_panel_rows[2].find("span",{"itemprop":"height"}).text
                    weight = info_panel_rows[2].find("span",{"itemprop":"weight"}).text
                else: # Executes this path if the player has nicknames
                    if (info_panel_rows[2].find("strong") != None):
                        position = info_panel_rows[2].find("strong").next_sibling
                        height = info_panel_rows[3].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[3].find("span", {"itemprop": "weight"}).text
                    else:  # Special path for players with a different birthname and nickname. Ex: Willie Cauley-Stein
                        position = info_panel_rows[3].find("strong").next_sibling
                        height = info_panel_rows[4].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[4].find("span", {"itemprop": "weight"}).text

                    # Testing output
                    # print(full_name)
                    # print(height)
                    # print(weight)
                    # print(team)
            position = position.encode('ascii', 'ignore').strip()
            position = position.decode()
            print(position) # Skipping position for now due to weird output. Posted a Stack Overflow question

            # Create a CSV to append all od the gathered data to
            with open(os.path.join(PLAYERS_DIRECTORY, (player_name + '.csv')), 'w', newline='') as f:  # Create a CSV for the current team
                writer = csv.writer(f)  # Create a writer for the csv
                # Write to the CSV all of the gathered data
                writer.writerow(["team",team_name])
                writer.writerow(["player webpage",player_url])
                writer.writerow(["playerID",player_id])
                writer.writerow(["full name",full_name])
                writer.writerow(["position"])
                writer.writerow(["height",height])
                writer.writerow(["weight",weight])
    return

# Input   : Teams to check injury list for
# Output  : New Injuries.csv and updated injury tables for the chosen teams
# Purpose : Used to update the injuries in the Injuries csv and given teams csv's to allow for the user to check who is injured before a game to give them accurate results.
def injury_update():
    return
# Input   : Amount of years to scrape.
# Output  : CSV files for players with data up to given amount of years
# Purpose : General purpose scraper for large data.
#TODO - Check if there exist players CSVs in the directory
#     - Change to work iteratively over a number of years
#     - Add some headers identifying what years have been scraped already in the CSV
def scrape(years = [str(date.today().year)]):
    for file in os.listdir(PLAYERS_DIRECTORY):
        filepath = (os.path.join(PLAYERS_DIRECTORY,file))
        print(filepath)
        with open(filepath,'r') as csvIn:
            csvIn = csv.reader(csvIn)
            csv_listified = list(csvIn)
            print(csv_listified)
            player_id = csv_listified[2][1]
        print(player_id)
        curr_year_stats_url = BASE_URL + "/players" + player_id + "gamelog/" + years[0]
        print(curr_year_stats_url)
        driver.get(curr_year_stats_url)
        soup = BeautifulSoup(driver.page_source,'lxml')
        if(soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all("tr") == None):
            continue
        else:
            table_check = soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all("tr")
        table_check = len(table_check)
        df = pandas.read_html(driver.page_source)
        if (table_check > 1):
            curr_year_stats = df[7]
        else:
            curr_year_stats = df[0]
        curr_year_stats = curr_year_stats.drop("Rk",1)
        curr_year_stats = curr_year_stats.drop("G",1)
        curr_year_stats = curr_year_stats.drop("Age",1)
        print(curr_year_stats)
        with open(filepath, 'a') as f:
            curr_year_stats.to_csv(f, header = True)
    return
# Testing
# Running time test
start_time = time.time()
TEAMS_DIRECTORY, PLAYERS_DIRECTORY = directory_builder()
#test_init = init_csvs()
test_scrape = scrape()
print("Execution time: " + str((time.time() - start_time)))

#TODO
# Scrape any info needed for the teams. Determine this with clients and Colin, taking out what will be unnecessary.
# Scrape player data
# Scrape injuries
# Integrate with a Main terminal program
# Make sure to prompt the user that when they use the init functions, any existing CSVs will be overwritten.