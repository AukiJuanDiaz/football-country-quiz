import requests
from bs4 import BeautifulSoup
from enum import Enum
import re
import os
import json
from generate_image import generate_the_guessing_image, generate_the_solution_image
from scraping_competition_data import download_team_logos, get_list_of_participants, get_list_of_match_numbers
from scraping_match_data import get_match_data

# INPUT PARAMETERS
base_url_match_reports = 'https://www.transfermarkt.de/spielbericht/index/spielbericht/'

# Url ot the particpants page of the competition
url_participants = 'https://www.transfermarkt.de/uefa-champions-league/teilnehmer/pokalwettbewerb/CL/saison_id/2021'

# Url to the page with all matches of the competition
url_matches = 'https://www.transfermarkt.de/uefa-champions-league/gesamtspielplan/pokalwettbewerb/CL/saison_id/2021'

# Competion abbreviation used for folder name
competition = 'CL2122'

# Define headers to make the request look more human
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


if __name__ == "__main__":
    # Make sure the directory exists
    directory = f'data_gathering/images/{competition}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Send a GET request to the URL with the headers and store the response in a variable
    response = requests.get(url_participants, headers=headers)
    soup_participants = BeautifulSoup(response.content, 'html.parser')

    # Get the List of Participants and download their team logos
    participants_names = get_list_of_participants(soup_participants, competition)
    download_team_logos(soup_participants, competition)

    # Send a GET request to the URL with the headers and store the response in a variable
    response = requests.get(url_matches, headers=headers)
    soup_matches = BeautifulSoup(response.content, 'html.parser')
    match_numbers = get_list_of_match_numbers(soup_matches, competition)

    for i in range(len(match_numbers)):
        match_number = match_numbers[i]
        print(match_number)

        # Send a GET request to the URL with the headers and store the response in a variable
        url = base_url_match_reports + match_number
        response = requests.get(url, headers=headers)
        soup_match = BeautifulSoup(response.content, 'html.parser')

        match_data = get_match_data(soup_match, match_number)

        # Store the match data as a json in a new folder
        # The folder is named after the match number of the game
        # Navigate up one level to /home/user/
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        folder_path_competition = f"football-country-quiz\static\competition_data\{competition}"
        joined_path_competition = os.path.join(parent_dir, folder_path_competition)
        new_folder_for_match = os.path.join(joined_path_competition, str(match_number))

        # Create the new folder if it doesn't already exist
        if not os.path.exists(new_folder_for_match):
            os.makedirs(new_folder_for_match)

        # Create the path to the json file
        json_file_path = os.path.join(new_folder_for_match, "match_data.json")

        # Save the match_data dictionary as a JSON file inside the new folder
        with open(json_file_path, "w") as f:
            json.dump(match_data, f)

        # Call a function to generate the guessing and the solution image
        generate_the_guessing_image(match_data)
        generate_the_solution_image(match_data)

    print("Done!")