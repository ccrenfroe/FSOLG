import csv
import os
import glob
import pandas as pd
from pathlib import Path

#Constants
WEEK = 4
DOUBLE_WEEK = 8
fieldnames = ['Started', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
              'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']

PROGRAM_ROOT = str(Path(__file__).resolve().parent.parent)

def directory_builder():
    if (os.path.isdir(PROGRAM_ROOT + "/Data") == False):
        os.makedirs(PROGRAM_ROOT + '/Data/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Teams/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Players/')
        os.makedirs(PROGRAM_ROOT + '/Data/Basketball/Averages/')
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams/'),
                (PROGRAM_ROOT + '/Data/Basketball/Players'),
                (PROGRAM_ROOT + '/Data/Basketball/Averages'))
    else: # Data directory exists
        return ((PROGRAM_ROOT + '/Data/Basketball/Teams'),
                (PROGRAM_ROOT + '/Data/Basketball/Players'),
                (PROGRAM_ROOT + '/Data/Basketball/Averages'))


TEAM_DIRECTORY, PLAYERS_DIRECTORY, AVERAGES_DIRECTORY = directory_builder()


os.chdir(PLAYERS_DIRECTORY)

extension = 'csv'

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


i = 0
for player in all_filenames[:14]:
    dataset = pd.read_csv(player, skiprows=11)
    dataset['Started'] = pd.to_numeric(dataset['Started'])
    print(player)
    print(dataset)

    os.chdir(AVERAGES_DIRECTORY)
    if i == 0:

        with open('ZZ1.csv', mode='w', newline='', encoding='utf-8') as player_file:
            player_writer = csv.writer(player_file)
            player_writer.writerow(fieldnames)
            player_writer.writerow(dataset[-WEEK:].mean(skipna=True))

        with open('ZZ2.csv', mode='w', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(fieldnames)
            player_writer.writerow(dataset[-DOUBLE_WEEK:].mean(skipna=True))

        with open('ZZF.csv', mode='w', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(fieldnames)
            player_writer.writerow(dataset.mean(skipna=True))

        with open('ZZA.csv', mode='w', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(fieldnames)
            player_writer.writerow(dataset[-1:].mean(skipna=True))

        os.chdir(PLAYERS_DIRECTORY)
        i += 1

    else:

        os.chdir(AVERAGES_DIRECTORY)
        with open('ZZ1.csv', mode='a') as player_file:
            player_writer = csv.writer(player_file)
            player_writer.writerow(dataset[-WEEK:].mean(skipna=True))

        with open('ZZ2.csv', mode='a', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(dataset[-DOUBLE_WEEK:].mean(skipna=True))

        with open('ZZF.csv', mode='a', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(dataset.mean(skipna=True))

        with open('ZZA.csv', mode='w', newline='') as player_file:
            player_writer = csv.writer(player_file,  delimiter=",")
            player_writer.writerow(fieldnames)
            player_writer.writerow(dataset[-1:].mean(skipna=True))

        os.chdir(PLAYERS_DIRECTORY)