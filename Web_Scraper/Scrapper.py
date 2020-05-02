# Web Scrapper for NBA.com
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# Imports here
import pandas
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from datetime import  datetime as dt
import csv
from bs4 import BeautifulSoup
from datetime import date
import os
from pathlib import Path
import unidecode
import time

# Global variables here
DELAY = 5
TOTAL_NBA_TEAMS = 30
BASE_URL = "https://www.basketball-reference.com"
TEAMS = ['ATL','BOS','BRK','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND', 'LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS'] # Current NBA teams. Abbreviations are according to basketball-reference.com
PROGRAM_ROOT = str(Path(__file__).resolve().parent.parent)
csvHeaders = ['Date','Team','Home/Away','Opp','Result Spread','Started','Minutes Played','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','GmSc','+/-']

# Webdriver
#driver = webdriver.Chrome() # Add extension of whatever driver you are using. For example, I am using Chromium, so I have it as webdriver.Chrome(). If you are using firefox, it would be webdriver.Firefox().

def directory_builder():
    if (os.path.isdir(PROGRAM_ROOT + "/Data") == False):
        os.makedirs(PROGRAM_ROOT + '/Data/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Teams/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Players/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Salaries/')
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'), (PROGRAM_ROOT + '/Data/Basketball/Players/'), (PROGRAM_ROOT + '/Data/Basketball/Salaries/'))
    else: # Data directory exists
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'), (PROGRAM_ROOT + '/Data/Basketball/Players/'), (PROGRAM_ROOT + '/Data/Basketball/Salaries/'))

# Input  : None
# Output : Outputs a new CSV for each team and players with basic data.
# Purpose: Makes initial CSVs for every team and player. This is done when the user wants to start fresh. An example case could be if the user wants to start fresh for a new season.
def init_csvs():
    driver = webdriver.Chrome()
    TEAMS_DIRECTORY, PLAYERS_DIRECTORY, SALARIES_DIRECTORY = directory_builder()
    for team in TEAMS:
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
        if ("Description" in df[1].columns): # If the table has a description column, that means its the injury table
            injuries = df[1].loc[:,"Player"]

        # Create a CSV to append all od the gathered data to
        with open(os.path.join(TEAMS_DIRECTORY, (team_name + '.csv')), 'w', newline='', encoding='utf-8') as f: # Create a CSV for the current team
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

            player_url = BASE_URL + link['href'] # Build the URL for the players webpage
            driver.get(player_url)
            soup = BeautifulSoup(driver.page_source,'lxml')
            info_panel = soup.find("div",{"id":"meta"}) # Focus on the section of the page with all of the basic player info needed
            player_name = info_panel.find("h1",{"itemprop":"name"}).text # Get the players name
            info_panel_rows = info_panel.find_all("p") # Find each row of info in the info_panel section


            # This section is split up into different cases. The 2 main cases are if the first row is a pronunciation row or not. From there, it is also broken up into if the player had a previous name or not, as well as a nickname. This matters as the differences cascade the rows, causing the indexes to change.
            if (info_panel_rows[0].find("strong").text == "Pronunciation"): # First row is pronunciation
                full_name = info_panel_rows[1].find("strong").find("strong").text # Get the players full name. Useful in case there are players with the same names that need to be distinguished between.
                if(info_panel_rows[2].find("strong") != None): # Executes this path if there is no nickname line for the player
                    position = info_panel_rows[2].find("strong").next_sibling # Get the position. Currently bugged and giving weird output
                    height = info_panel_rows[3].find("span",{"itemprop":"height"}).text # Get height
                    weight = info_panel_rows[3].find("span",{"itemprop":"weight"}).text # Get weight
                    if info_panel_rows[-1].find("strong").text.strip() == "Experience:": # Check if the Experience column exists
                        experience = info_panel_rows[-1].find("strong").next_sibling
                    else:
                        experience = "NA"
                else: # Executes this path if the player has nicknames
                    if(info_panel_rows[3].find("strong") != None): # Normal path
                        position = info_panel_rows[3].find("strong").next_sibling
                        height = info_panel_rows[4].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[4].find("span",{"itemprop":"weight"}).text
                        if info_panel_rows[-1].find("strong").text.strip() == "Experience:":
                            experience = info_panel_rows[-1].find("strong").next_sibling
                        else:
                            experience = "NA"
                    else: # Special path for players with a different birthname and nickname. Ex: Bismack Biyombo
                        position = info_panel_rows[4].find("strong").next_sibling
                        height = info_panel_rows[5].find("span",{"itemprop":"height"}).text
                        weight = info_panel_rows[5].find("span",{"itemprop":"weight"}).text
                        if info_panel_rows[-1].find("strong").text.strip() == "Experience:":
                            experience = info_panel_rows[-1].find("strong").next_sibling
                        else:
                            experience = "NA"
            else:
                full_name = info_panel_rows[0].find("strong").find("strong").text
                if(info_panel_rows[1].find("strong") != None): # Executes this path if there is no nickname line for the player
                    position = info_panel_rows[1].find("strong").next_sibling
                    height = info_panel_rows[2].find("span",{"itemprop":"height"}).text
                    weight = info_panel_rows[2].find("span",{"itemprop":"weight"}).text
                    if info_panel_rows[-1].find("strong").text.strip() == "Experience:":
                        experience = info_panel_rows[-1].find("strong").next_sibling
                    else:
                        experience = "NA"
                else: # Executes this path if the player has nicknames
                    if (info_panel_rows[2].find("strong") != None):
                        position = info_panel_rows[2].find("strong").next_sibling
                        height = info_panel_rows[3].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[3].find("span", {"itemprop": "weight"}).text
                        if info_panel_rows[-1].find("strong").text.strip() == "Experience:":
                            experience = info_panel_rows[-1].find("strong").next_sibling
                        else:
                            experience = "NA"
                    else:  # Special path for players with a different birthname and nickname. Ex: Willie Cauley-Stein
                        position = info_panel_rows[3].find("strong").next_sibling
                        height = info_panel_rows[4].find("span", {"itemprop": "height"}).text
                        weight = info_panel_rows[4].find("span", {"itemprop": "weight"}).text
                        if info_panel_rows[-1].find("strong").text.strip() == "Experience:":
                            experience = info_panel_rows[-1].find("strong").next_sibling
                        else:
                            experience = "NA" # Experience row wasn't on page, so put NA
            position = position.encode('ascii', 'ignore').strip()
            position = position.decode()
            experience = experience.strip()

            # Create a CSV to append all od the gathered data to
            with open(os.path.join(PLAYERS_DIRECTORY, (player_name + '.csv')), 'w', newline='', encoding='utf-8') as f:  # Create a CSV for the current team
                writer = csv.writer(f)  # Create a writer for the csv
                # Write to the CSV all of the gathered data
                writer.writerow(["team",team_name])
                writer.writerow(["player webpage",player_url])
                writer.writerow(["playerID",player_id])
                writer.writerow(["full name",full_name])
                writer.writerow(["position",position])
                writer.writerow(["height",height])
                writer.writerow(["weight",weight])
                writer.writerow(["Experience",experience])
                writer.writerow(["Dates Scraped (Oldest to Newest)","0001-01-01","0001-01-01"])
                writer.writerow([""])
                writer.writerow(['DATA'])
                writer.writerow(csvHeaders)
    return

# Input   : Teams to check injury list for
# Output  : New Injuries.csv and updated injury tables for the chosen teams
# Purpose : Used to update the injuries in the Injuries csv and given teams csv's to allow for the user to check who is injured before a game to give them accurate results.
def injury_update():
    return
# Input   : List of years to scrape.
# Output  : CSV files for players with data up to given amount of years
# Purpose : General purpose scraper for large data.
#TODO - Check if there exist players CSVs in the directory
#     - Add some headers identifying the date range scraped already. Located in row 7 element 2 and 3
def scrape(years = [str(date.today().year)]):
    driver = webdriver.Chrome()
    TEAMS_DIRECTORY, PLAYERS_DIRECTORY, SALARIES_DIRECTORY = directory_builder()
    # Goes through each player and scrapes the stats for each year given by the input parameter.
    for year in years:
        i = 0 # Counter to keep track of iterations
        for file in os.listdir(PLAYERS_DIRECTORY):
            filepath = (os.path.join(PLAYERS_DIRECTORY,file))
            with open(filepath,'r', encoding='utf-8') as csvIn:
                csvIn = csv.reader(csvIn)
                csv_listified = list(csvIn)
                print(csv_listified)
                player_id = csv_listified[2][1] # Needed to find the html webpages of the player

                ##LOW PRIORITY. IMPLEMENT LATER IF TIME.
                ######################################################################################
                # curr_newest_date = csv_listified[7][2]  # Get the current most recent date         #
                # curr_newest_date = dt.strptime(curr_newest_date, "%Y-%m-%d").date()                #
                # curr_oldest_date = csv_listified[7][1]  # Get the current oldest date              #
                # curr_oldest_date = dt.strptime(curr_oldest_date, "%Y-%m-%d").date()                #
                ######################################################################################

            curr_year_stats_url = BASE_URL + "/players" + player_id + "gamelog/" + str(year) # Build the URL string
            driver.get(curr_year_stats_url)
            soup = BeautifulSoup(driver.page_source,'lxml')
            # Skips over this year if there are no tables found, as in there is no games the player played in this year.
            if((soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}) == None) or (soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all("tr") == None )):
                continue
            else:
                table_check = soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all("tr")
            table_check = len(table_check) # Check for later step
            df = pandas.read_html(driver.page_source) # Take in the whole table of stats for the player
            # Depending on the layout of the page, the table is located at a different part in the df list. (This is the later step mentioned)
            if (table_check > 1):
                curr_year_stats = df[7]
            else:
                curr_year_stats = df[0]

            #Drop unnecessary columns
            curr_year_stats = curr_year_stats.drop("Rk",1)
            curr_year_stats = curr_year_stats.drop("G",1)
            curr_year_stats = curr_year_stats.drop("Age",1)

            ######################################################################################
            # # Find the first and last date in the table                                        #
            # oldest_date = curr_year_stats.iloc[0]['Date']                                      #
            # oldest_date = dt.strptime(oldest_date, "%Y-%m-%d").date()                          #
            # newest_date = curr_year_stats.iloc[-1]['Date']                                     #
            # newest_date = dt.strptime(newest_date, "%Y-%m-%d").date()                          #
            ######################################################################################

            ############################################################################################################################################################################
            # # Need to update the dates since one is different, So need to create a new csv. Check both at once first and then check individually.
            # print(csv_listified[7][2] + "Current Newest Date")
            # print(csv_listified[7][1] + "Current Oldest Date")
            # # Enters this loop if a new CSV needs to be created because the dates need to be updated.i = i + 1
            # if ((curr_newest_date  < newest_date) or (curr_oldest_date > oldest_date) or (str(curr_oldest_date == "0001-01-01"))):
            #     if(curr_newest_date < newest_date): # Update the newest date if the newest date in the current table is a more recent date than the current
            #         csv_listified[7][2] = newest_date
            #     if(curr_oldest_date > oldest_date): # Update the oldest date if the oldest date in the current table is older than the current
            #         csv_listified[7][1] = oldest_date
            #     elif (str(curr_oldest_date) == "0001-01-01"): #Edge case for first Oldest date in.
            #         csv_listified[7][1] = oldest_date
            #
            #     # Create new CSV and copy all of the data over.
            #     with open(filepath,'w') as newCSV:
            #         writer = csv.writer(newCSV)
            #         writer.writerows(csv_listified) # Write over the old data
            #         curr_year_stats.to_csv(newCSV, header = True) # Add the new table of data
            ############################################################################################################################################################################
            with open(filepath, 'a') as f:
                curr_year_stats.to_csv(f,index=False, header = False) # Append the new table of data to the CSV file
        print(str(i) + " of 496 done")
    return
# Input   : Takes in a number of games to scrape and the year to start at.
# Output  : Update the CSV with the amount of games requested
# Purpose : Gives the user the ability to scrape a specific number of games as another scraping option.
def scrape_games(games, year):
    driver = webdriver.Chrome()
    TEAMS_DIRECTORY, PLAYERS_DIRECTORY, SALARIES_DIRECTORY= directory_builder()
    # Goes through each player and scrapes the stats for each year given by the input parameter.
    for file in os.listdir(PLAYERS_DIRECTORY):
        filepath = (os.path.join(PLAYERS_DIRECTORY, file))
        with open(filepath, 'r', encoding='utf-8') as csvIn:
            csvIn = csv.reader(csvIn)
            csv_listified = list(csvIn)
            player_id = csv_listified[2][1]  # Needed to find the html webpages of the player
            experience = csv_listified[7][1].split(' ')[0]
        i = 0
        current_year = year
        years_done = 0
        while (i < games and str(years_done) != experience): # Keep looping until we hit the number of games requested or if we have iterated back to the beginning of the players career
            curr_year_stats_url = BASE_URL + "/players" + player_id + "gamelog/" + str(current_year)  # Build the URL string
            driver.get(curr_year_stats_url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # Skips over this year if there are no tables found, as in there is no games the player played in this year.
            if ((soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}) == None) or (soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all("tr") == None)):
                if experience == "Rookie": # If its a rookie and we find no gamelog for this year, that means they were never plaing this year to begin with, so set i to a high number to break the while loop check and move on to the next player.
                    i = 99999;
                elif experience == "NA": # Same if the experience is NA
                    i = 99999;
                current_year = current_year -1 # Decrement the year to scrape the next year back in the next iteration
                continue
            else:
                table_check = soup.find("div", {"id": "game_log_summary_1", "class": "data_grid_box"}).find_all(
                    "tr")
            table_check = len(table_check)  # Check for later step
            df = pandas.read_html(driver.page_source)  # Take in the whole table of stats for the player
            # Depending on the layout of the page, the table is located at a different part in the df list. (This is the later step mentioned)
            if (table_check > 1):
                curr_year_stats = df[7]
            else:
                curr_year_stats = df[0]
            
            # Drop unnecessary columns
            curr_year_stats = curr_year_stats.drop("G", 1)
            curr_year_stats = curr_year_stats.drop("Age", 1)
            num_rows = curr_year_stats.iloc[-1]['Rk']
            curr_year_stats = curr_year_stats.drop("Rk", 1)

            with open(filepath, 'a') as f:
                if (i + int(num_rows) <= games):
                    curr_year_stats.to_csv(f, index=False, header=False)  # Append the new table of data to the CSV file
                    i = i + int(num_rows)
                    current_year = current_year -1
                    years_done = years_done + 1
                else:
                    for j in range(len(curr_year_stats)):
                        if (i < games):
                            curr_year_stats.loc[[j]].to_csv(f, index=False, header=False,mode='a')
                            i = i + 1
                    current_year = current_year - 1
                    years_done = years_done + 1

# Input   : Nothing.
# Output  : Outputes csvs with their respective players historical data on their fantasy salaries in the "Salaries" folder.
# Purpose : Allows for the gathering of the salaries to be used in the calculations and machine learning.
def salary_scrape():
    driver = webdriver.Chrome() # Start the driver up
    TEAMS_DIRECTORY, PLAYERS_DIRECTORY, SALARIES_DIRECTORY = directory_builder()
    for file in os.listdir(PLAYERS_DIRECTORY): # Go through each player
        filepath = (os.path.join(PLAYERS_DIRECTORY, file))
        with open(filepath, 'r', encoding='utf-8') as csvIn:
            name = filepath.split('/')[-1] # Split the last part of the filepath to just get the csv part of the filepath.
            name = unidecode.unidecode(name) # Gets rid of any special characters or letters with squigglies and apostrophes.
            # This is done so that the program accounts for last names that include 2 parts, such as a Doe Jr.
            # Bunch of operations to get the name formatted correctly to be compared against the names on the website
            ####
            name = name.split(" ",1)
            first_name = name[0]
            last_name = name[1]
            last_name = last_name.split('.csv')[0].capitalize()
            name = (last_name + ", " + first_name).upper() # Player name to be searched for on the website
            first_letter = last_name[0] # This is used to determine which path to take later
            #print(first_letter) testing output
            filename = first_name + " " + last_name + " Salary.csv" # name of the file to be outputted with the data
            #print(filename) testing output
            driver.get("http://rotoguru1.com/cgi-bin/playrh.cgi?0") # Go to the root webpage
            soup = BeautifulSoup(driver.page_source,'lxml') # lxml is a little faster, so opt for this instead of html.parser

            #print("CURRENT PLAYER : " + name) testing output
            #Try except block to try and find the select boxes again if they arent found on page load. Sometimes it needs to wait longer and then try again.
            try:
                A_to_K_Select = driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[1]/form/select")
                K_to_Z_Select = driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/select")
            except:
                time.sleep(1) # Waits one second and then tries to find the selects again.
                A_to_K_Select = driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[1]/form/select")
                K_to_Z_Select = driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/select")

            if(ord(first_letter) < ord("L")): # Compare the first letter of the name to L to determine which path to enter
                # Name before L
                for option in A_to_K_Select.find_elements_by_tag_name('option'): # Loop through each option until a match is found
                    if option == None: # If no match is found, eventually will get a nonetype and then prompt to the user that the player could not be found
                        print("PLAYER NOT LISTED")
                        break
                    if  (name in option.text.upper()): # If the name matches the current option
                        option.click() # select the option 
                        # print("Found " + option.text) Testing output
                        driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[1]/form/input").click() # Click the go button to go to the players stats page.
                        # Try except in case the element is not found on the first try
                        try: # If the option is there and can be clicked, click it
                            if(driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()): # Expand to show the full season history
                                driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()
                        except: # Try again after waiting 1 second.
                            time.sleep(1)
                            if(driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()): # Expand to show the full season history
                                driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()
                                #print("GOT IT IN THE ELSE LOOP") testing output
                        # Same thing, tries again if the code fails on the first time
                        try: # to data frame-ify the tables on the page
                            df = pandas.read_html(driver.page_source)
                            df = df[5] # The 5th table is the table needed
                        except: # Wait 1 second and then try again
                            time.sleep(1)
                            df = pandas.read_html(driver.page_source)
                            df = df[5] # Need the 5th table
                        # Drop useless columns and rows to neaten the output dataframe
                        df = df.drop([0,1,2,3,5,6,7,8,9], axis = 0) 
                        df = df.drop([1,2,3,5,7,8], axis = 1)
                        df = df.dropna()
                        #print(df) Testing output
                        # Write the dataframe to a new salary csv for the player.
                        with open(os.path.join(SALARIES_DIRECTORY, (filename)), 'w', newline='', encoding='utf-8') as f:  # Create a CSV for the current team
                            df.to_csv(f,index = False, header = False) # Append the new table of data to the CSV fil
                        break # Break and go to the next elemnt
            else:
                # Name after L
                for option in K_to_Z_Select.find_elements_by_tag_name('option'): # Loop through each option until a match is found
                    if option == None: # If no match is found, eventually will get a nonetype and then prompt to the user that the player could not be found
                        print("PLAYER NOT LISTED")
                        break
                    if (name.upper() in option.text.upper()):
                        option.click() # If the name matches the current option
                        #print("Found" + option.text) Testing output 
                        driver.find_element_by_xpath("/html/body/font/center/font/font[1]/p/a/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/input").click() # Click the go button to go to the players stats page.
                        # Try except in case the element is not found on the first try   
                        try: # If the option is there and can be clicked, click it
                            if(driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a")): # Expand to show the full season history
                                driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()
                        except: # Try again after waiting 1 second.
                            time.sleep(1)
                            if(driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a")): # Expand to show the full season history
                                driver.find_element_by_xpath("/html/body/font/center/font/font/table/tbody/tr[2]/td/center[1]/a").click()
                                #print("GOT IT IN THE ELSE LOOP") Testing output         
                        try: # Same thing, tries again if the code fails on the first time
                            df = pandas.read_html(driver.page_source)
                            df = df[5]
                        except: # Wait 1 second and then try again
                            time.sleep(1)
                            df = pandas.read_html(driver.page_source)
                            df = df[5] # Need the 5th table
                        # Drop useless columns and rows to neaten the output dataframe
                        df = df.drop([0,1,2,3,5,6,7,8,9], axis = 0)
                        df = df.drop([1,2,3,5,7,8], axis = 1)
                        df = df.dropna()
                        #print(df) Testing output
                        with open(os.path.join(SALARIES_DIRECTORY, (filename)), 'w', newline='', encoding='utf-8') as f:  # Create a CSV for the current team
                            df.to_csv(f,index=False, header = True) # Append the new table of data to the CSV fil
                        break # Break and go to the next elemnt

# Used in the FSOLG Program
def web_scrape(first_run, scrape_start, scrape_end, num_games, scrape_strat):

    start_time = time.time()
    if(first_run == True):
        init_csvs()

    if(scrape_strat == True):
        scrape([scrape_start, scrape_end])

    if(scrape_strat == False):
        scrape_games(num_games, 2020)

    print("Execution time: " + str((time.time() - start_time)))

# Used for testing
def main():
    start_time = time.time()
    #init_csvs()
    #scrape([2020,2019,2018])
    salary_scrape();
    print("Execution time: " + str((time.time() - start_time)))
    
#if __name__ == '__main__':
    #main()
# TODO
# Scrape injuries