# Command Line Interface
# By Caleb Renfroe & Colin Heaning AKA CoCa
# FSOLG

# importing the frameworks used inside of the CLI

# python library which facilitates the construction of CLI
import click
# formatting library for title
from pyfiglet import Figlet
# library to assist in presentation of commands
from funcy import identity

'''
'''
def simple_CLI():
    """Generate a user friendly form of the CLI
    The function calls the other components and prints to console
    @return: none
    """

    print("")
    print("Welcome to the Fantasy Sports Optimal Lineup Generator!")

    # Current implementation is for basketball alone,
    # Code is being developed to allow for easy implementation of new sports
    print("Please select the sport you are interested in: ")
    print("A) Basketball \n"
          "B) Other")
    curr_input = input("\nEnter the letter of the option: ")
    if curr_input == ('A').lower():
        current_sport = "Basketball"
    else:
        print("Other sports are not supported by FSOLG in the current version, defaulting to basketball")
        current_sport = "Basketball"

    print("")
    # CLI gathers the input and calls the other components
    print("What would you like to do with Basketball?")
    print("A) Update Data \n"
          "B) Retrain Machine Learning Algorithm \n"
          "C) Generate a fantasy lineup")
    curr_input = input("\nEnter the letter of the option: ")

    if curr_input == ("A").lower():
        print("Specified operation: Update Data")
        current_operation = "update"
        updateData()

    elif curr_input == ("B").lower():
        print("Specified operation : Retrain Machine Learning Algorithm")
        current_operation = "retrain"
        retrainData()

    elif curr_input == ("C").lower():
        print("Specified operation: Generate a fantasy lineup")
        current_operation = "generate"
        generateLineup()

    # Defaulting to lineup generation allows for quicker obtainment of lineups
    else:
        print("Unrecognized operation, defaulting to lineup generation")
        current_operation = "generate"
        generateLineup()


def updateData():
    """Updating the stored data by calling the web scraper
    Nothing is returned to the CLI, it only prints success to the console
    @return: nothing
    """

    print("-----------------------------------------------------")
    print("")
    print("How far back would you like to scrape data?")
    scrape_size = input("Specify as a whole number of days:   ")
    print("-----------------------------------------------------")
    # Web Sraping Component is connected here
    # scrape(scrape_size)

def retrainData():
    """Adjusting the current training and testing set
    of the Machine Learning Model currently maintained
    @return: nothing
    """

    print("-----------------------------------------------------")
    print("")
    print("How many days would you like to train the ML model on? Specify 'ALL' to train on the whole set.")
    training_size = input("Specify as a whole number of days or ALL:   ")
    print("-----------------------------------------------------")
    # Machine Learning Component is connected here
    # train(training_size)

def generateLineup():
    """Generate the fantasy lineup with current ML model
    @return: Fantasy lineup in list form printed to console
    """

    print("-----------------------------------------------------")
    print("")
    # Fantasy site determines pricing for the algorithm
    print("Please specify the Fantasy draft website or application being used for the lineup.")
    fantasy_site = input("(A) DraftKings or "
                          "(B) FanDuel"
                          ":   ")
    print("-----------------------------------------------------")
    # Machine Learning Component is connected here
    # generate_Lineup(fantasy_site)
    # It will return a list of players that will be printed here in the CLI

# Defining the CLI command that operates the program (the default advanced CLI)
@click.command()

# Verbosity flag to allow for a clearer understanding of what is happening
@click.option('--verbose', "-v",
              is_flag=True,
              required=False,
              help="Prints verbose version of program output.",
              type=click.STRING,)

# Defining the sport via its own individual flag
@click.option("--basketball", "-b",
              is_flag=True,
              required=False,
              help="Specified lineup for fantasy basketball",
              type=click.STRING,)

# Specifying the update operation flag
@click.option("--update", "-u",
              is_flag=True,
              required=False,
              help="Pull and update data for sport from current web statistics",
              type=click.STRING,)

# Specifying the retrain operation flag
@click.option("--retrain", "-r",
              is_flag=True,
              required=False,
              help="Alter the machine learning algorithm's weights and parameters",
              type=click.STRING,)

# Specifying the generate lineup operation flag
@click.option("--generate", "-g",
              is_flag=True,
              required=False,
              help="Generate the lineup of players for the specified sport",
              type=click.STRING,)

# Specifying the simple CLI request flag
@click.option('--simple', "-s",
              is_flag=True,
              required=False,
              help="Switches the CLI to a simpler to use, dictated format",
              type=click.STRING,)


def process(verbose, basketball, update, retrain, generate, simple):
    """User interface component of the Fantasy Sports Optimal Lineup Generator"""

    # a beautified title for the initial program launch
    print("==================================================")
    title = Figlet(font='slant')
    print(title.renderText("F S O L G"))
    print("==================================================")

    # Setting the default CLI status to advanced
    simple_run = False

    # If the simple flag is detected, switch to it and stop the advanced CLI
    if simple:
        print("Request to switch to simple CLI detected")
        print("Switching....")
        simple_CLI()
        simple_run = True

    # Simple CLI not requested, check flags and run without repeated interaction
    if not simple_run:

        # Define a function to print if the verbose flag is detected
        verbose_print = print if verbose else identity

        verbose_print("Verbose mode activated.")

        verbose_print("Determining specified sport for lineup operations...")
        if basketball:
            # current_sport is unused whilst only a single sport is implemented
            current_sport = "basketball"
            verbose_print("Specified sport is: Basketball.")
        else:
            verbose_print("Alternate sports are unsupported in FSOLG's current version")
            verbose_print("Defaulting to basketball")

        verbose_print("Determining specified operation for current sport...")
        if update:
            verbose_print("Specified operation detected: update")
            current_operation = "update"
            updateData()

        elif retrain:
            verbose_print("Specified operation detected: retrain machine learning model")
            current_operation = "retrain"
            retrainData()

        elif generate:
            verbose_print("Specified operation detected: generate lineup")
            current_operation = "generate"
            generateLineup()

# Main simply calls the CLI command
if __name__ =="__main__":
    process()