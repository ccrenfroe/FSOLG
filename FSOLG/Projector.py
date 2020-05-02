# Fantasy Point Projector
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

import csv
import math
import os
import glob
import pandas as pd
from pathlib import Path
from collections import OrderedDict

#Constants
WEEK = 4
DOUBLE_WEEK = 8
fieldnames = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
              'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']
projection_names = ['FP']
PROGRAM_ROOT = str(Path(__file__).resolve().parent.parent)
player_names = []

#Same directory builder as the scraper however this simply builds the averages and projections
def directory_builder():
    if not os.path.isdir(PROGRAM_ROOT + "/Data/Basketball/Averages"):
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Averages/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Projections/')
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'),
                (PROGRAM_ROOT + '/Data/Basketball/Players/'),
                (PROGRAM_ROOT + '/Data/Basketball/Averages/'),
                (PROGRAM_ROOT + '/Data/Basketball/Projections/'))
    else: # Data directory exists
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'),
                (PROGRAM_ROOT + '/Data/Basketball/Players/'),
                (PROGRAM_ROOT + '/Data/Basketball/Averages/'),
                (PROGRAM_ROOT + '/Data/Basketball/Projections/'))

def get_names():
    TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()
    os.chdir(PLAYERS_DIRECTORY)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    for player in all_filenames:
        player_names.append(player[:-4])
    os.chdir(AVERAGES_DIRECTORY)

def generate_averages():
    """Take the scraped input and generate useful statistics
    This function intakes scraped csv's cleans them, and produces mean statistics
    into a more streamlined collection of csv's
    @return: none
    """

    # Build the directories/check if they are built already
    TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()

    os.chdir(PLAYERS_DIRECTORY)

    # Obtain all of the file names contained in the scraped players folder
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    i = 0
    # Going through each player in order to clean and average their data
    for player in all_filenames:

        # For the purposes of averages, the first 6 columns are undesirable, along with the first 11 rows
        dataset = pd.read_csv(player, skiprows=11, usecols=range(7, 27))
        dataset = dataset[dataset.FGA != 'Inactive']
        dataset = dataset[dataset.FGA != 'Did Not Play']
        dataset = dataset[dataset.FGA != 'Did Not Dress']
        dataset = dataset[dataset.FGA != 'Not With Team']

        # This cleans the csv of the repeated stat header
        dataset = dataset[dataset.FGA != 'FGA']

        # An odd scrape of ",0" causes NaN to appear whenever a % was 0, this changes it to reflect the real stat
        for index, row in dataset.iterrows():

            if pd.isnull(row['FT%']):
                row['FT%'] = 0

            if pd.isnull(row['FG%']):
                row['FG%'] = 0

            if pd.isnull(row['3P%']):
                row['3P%'] = 0

        print("Processing... " + player[:-4])

        # Jump to the averages directory to place the combined stats
        os.chdir(AVERAGES_DIRECTORY)
        if i == 0:

            # Do not want to rewrite the csv every time, so write mode only occurs once
            with open('One_Week_Stats.csv', mode='w', newline='', encoding='utf-8') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
                # Averages for a week of games
                player_writer.writerow(dataset[-WEEK:].astype(float).mean(skipna=True))

            with open('Two_Week_Stats.csv', mode='w', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
                # Averages for two weeks worth of games
                player_writer.writerow(dataset[-DOUBLE_WEEK:].astype(float).mean(skipna=True))

            with open('Full_Season_Stats.csv', mode='w', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
                # Averages for the full season
                player_writer.writerow(dataset.astype(float).mean(skipna=True))

            os.chdir(PLAYERS_DIRECTORY)
            i += 1

        else:

            os.chdir(AVERAGES_DIRECTORY)
            with open('One_Week_Stats.csv', mode='a', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(dataset[-WEEK:].astype(float).astype(float).mean(skipna=True))

            with open('Two_Week_Stats.csv', mode='a', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(dataset[-DOUBLE_WEEK:].astype(float).mean(skipna=True))

            with open('Full_Season_Stats.csv', mode='a', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(dataset.astype(float).mean(skipna=True))

            os.chdir(PLAYERS_DIRECTORY)


def calculate_fantasy_points(site, strategy):
    """Take the provided statistics and apply site values to them
    This method creates the fantasy projections for the specified site according
    to the methods chosen
    @return: none
    """

    TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()

    # Determine which strategy is going to be used for this generation
    os.chdir(AVERAGES_DIRECTORY)
    if strategy == 1:
        dataset = pd.read_csv('One_Week_Stats.csv')
    elif strategy == 2:
        dataset = pd.read_csv('Two_Week_Stats.csv')
    else:
        dataset = pd.read_csv('Full_Season_Stats.csv')

    if site == 1:
        print("Fanduel")

        i = 0
        draft_dict = {}
        # The unique scoring of Fanduel calculated for the specific player
        for index, row in dataset.iterrows():
            points = (row['FG'] * 2) + (row['3P'] * 3) + (row['FT'] * 1)
            rebounds = (row['DRB'] + row['ORB']) * 1.2
            assists = row['AST'] * 1.5
            blocks = row['BLK'] * 3
            steals = row['STL'] * 2
            turnovers = row['TOV'] * (-1)

            fantasy_projection = points + rebounds + assists + blocks +\
                                 steals + turnovers

            get_names()
            draft_dict[player_names[i-1]] = fantasy_projection
            i += 1

        null_keys = list()

        for (key, value) in draft_dict.items():
            if math.isnan(value):
                null_keys.append(key)

        for key in null_keys:
            if key in draft_dict:
                del draft_dict[key]

        dd = OrderedDict(sorted(draft_dict.items(), key=lambda x: x[1]))
        for x in dd:
            print(x, "is projected to score: ", dd[x])


    # The unique scoring of Draftkings calculated for the specific player
    else:
        print("Draftkings")
        i = 1
        draft_dict = {}
        for index, row in dataset.iterrows():
            # Draftkings does simple points instead of separating them
            points = (row['FG'] * 2) + (row['3P'] * 3) + (row['FT'] * 1)
            three_point_bonus = row['3P'] * 0.5
            rebounds = (row['DRB'] + row['ORB']) * 1.25
            assists = row['AST'] * 1.5
            blocks = row['BLK'] * 2
            steals = row['STL'] * 2
            turnovers = row['TOV'] * (-.5)

            double_check = 0
            double_double = 0
            triple_double = 0

            # Draftkings considers the triple doubles and double doubles as bonus points so this tracks it
            if points >= 10:
                double_check += 1

            if assists >= 10:
                double_check += 1

            if rebounds >= 10:
                double_check += 1

            if blocks >= 10:
                double_check += 1

            if steals >= 10:
                double_check += 1

            if double_check >= 2:
                double_double = 1.5

            if double_check >= 3:
                triple_double = 3

            fantasy_projection = points + three_point_bonus + rebounds + assists + blocks + steals + turnovers + \
                                 triple_double + double_double

            get_names()
            draft_dict[player_names[i-1]] = fantasy_projection
            i += 1

        null_keys = list()

        for(key, value) in draft_dict.items():
            if math.isnan(value):
                null_keys.append(key)

        for key in null_keys:
            if key in draft_dict:
                del draft_dict[key]

        dd = OrderedDict(sorted(draft_dict.items(), key=lambda x: x[1]))
        for x in dd:
            print(x, "is projected to score: ", dd[x])

# Used to call the program from the FSOLG cli
def generate(site, strategy):

    calculate_fantasy_points(site, strategy)


def main():
    print(PROGRAM_ROOT)
    generate_averages()
    calculate_fantasy_points(1, 1)

#if __name__ == '__main__':
#    main()