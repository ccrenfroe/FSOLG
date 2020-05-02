import csv
import os
import glob
import pandas as pd
from pathlib import Path
import numpy

#Constants
WEEK = 4
DOUBLE_WEEK = 8
fieldnames = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
              'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']
projection_names = ['FP']

PROGRAM_ROOT = str(Path(__file__).resolve().parent.parent)


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


TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()
os.chdir(PLAYERS_DIRECTORY)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


def generate_averages():
    TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()
    i = 0

    for player in all_filenames:
        dataset = pd.read_csv(player, skiprows=11, usecols=range(7, 27))
        dataset = dataset[dataset.FGA != 'Inactive']
        dataset = dataset[dataset.FGA != 'Did Not Play']
        dataset = dataset[dataset.FGA != 'Did Not Dress']
        dataset = dataset[dataset.FGA != 'Not With Team']
        dataset = dataset[dataset.FGA != 'FGA']

        for index, row in dataset.iterrows():

            if pd.isnull(row['FT%']):
                row['FT%'] = 0

            if pd.isnull(row['FG%']):
                row['FG%'] = 0

            if pd.isnull(row['3P%']):
                row['3P%'] = 0

        print("Processing... " + player[:-4])
        print(dataset)

        os.chdir(AVERAGES_DIRECTORY)
        if i == 0:

            with open('One_Week_Stats.csv', mode='w', newline='', encoding='utf-8') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
                player_writer.writerow(dataset[-WEEK:].astype(float).mean(skipna=True))

            with open('Two_Week_Stats.csv', mode='w', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
                player_writer.writerow(dataset[-DOUBLE_WEEK:].astype(float).mean(skipna=True))

            with open('Full_Season_Stats.csv', mode='w', newline='') as player_file:
                player_writer = csv.writer(player_file,  delimiter=",")
                player_writer.writerow(fieldnames)
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
    TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY, PROJECTIONS = directory_builder()

    os.chdir(AVERAGES_DIRECTORY)
    if strategy == 1:
        dataset = pd.read_csv('One_Week_Stats.csv')
    elif strategy == 2:
        dataset = pd.read_csv('Two_Week_Stats.csv')
    else:
        dataset = pd.read_csv('Full_Week_Stats.csv')

    if site == 1:
        print("Fanduel")

        i = 0
        for index, row in dataset.iterrows():
            field_goals = row['FG'] * 2
            three_pointers = row['3P'] * 3
            free_throws = row['FT'] * 1
            rebounds = (row['DRB'] + row['ORB']) * 1.2
            assists = row['AST'] * 1.5
            blocks = row['BLK'] * 3
            steals = row['STL'] * 2
            turnovers = row['TOV'] * (-1)

            fantasy_projection = field_goals + three_pointers + free_throws + rebounds + assists + blocks +\
                                 steals + turnovers

            print(fantasy_projection)

            os.chdir(PROJECTIONS)
            if i == 0:
                with open('Projections.csv', mode='w', newline='', encoding='utf-8') as projection_file:
                    projection_writer = csv.writer(projection_file, delimiter=",")
                    projection_writer.writerow(projection_names)
                    #projection_writer.writerow(fantasy_projection)

            else:
                with open('Projections.csv', mode='a', newline='', encoding='utf-8') as projection_file:
                    projection_writer = csv.writer(projection_file, delimiter=",")
                    projection_writer.writerow(projection_names)
                    #projection_writer.writerow(fantasy_projection)

            os.chdir(AVERAGES_DIRECTORY)

    else:
        print("Draftkings")

        for index, row in dataset.iterrows():
            points = (row['FG'] * 2) + (row['3P'] * 3) + (row['FT'] * 1)
            three_point_bonus = row['3P'] * 0.5
            rebounds = (row['DRB'] + row['ORB']) * 1.25
            assists = row['AST'] * 1.5
            blocks = row['BLK'] * 2
            steals = row['STL'] * 2
            turnovers = row['TOV'] * (-.5)

            double_double_check = 0
            triple_double_check = 0
            double_double = 0
            triple_double = 0

            if points >= 10:
                double_double_check += 1

            if assists >= 10:
                double_double_check += 1

            if rebounds >= 10:
                double_double_check += 1

            if blocks >= 10:
                double_double_check += 1

            if steals >= 10:
                double_double_check += 1

            if double_double_check >= 2:
                double_double = 1.5

            if triple_double_check >= 3:
                triple_double = 3

            fantasy_projection = points + three_point_bonus + rebounds + assists + blocks + steals + turnovers + \
                                 triple_double + double_double

            print(fantasy_projection)

def generate(first_run, site, strategy):

    if(first_run == True):
        generate_averages()

    calculate_fantasy_points(site, strategy)



def main():
    print(PROGRAM_ROOT)
    generate_averages()
    calculate_fantasy_points(1, 1)

#if __name__ == '__main__':
#    main()