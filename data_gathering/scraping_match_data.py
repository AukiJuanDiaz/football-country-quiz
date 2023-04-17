
import requests
from bs4 import BeautifulSoup
from enum import Enum
import re
import os
import json
from generate_image import generate_the_guessing_image, generate_the_solution_image

"""
# URL of the match report
match_number = 3651082 # 4:0 von Ajax gegen BVB
# match_number = 3651068 # Sieg von Sheriff gegen Real
# match_number = 3714222 # Bayern 7:1 gegen Salzburg
# match_number = 3812391 # Finale
base_url = 'https://www.transfermarkt.de/spielbericht/index/spielbericht/'

url = base_url + str(match_number)



# Define headers to make the request look more human
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Send a GET request to the URL with the headers and store the response in a variable
response = requests.get(url, headers=headers)

# Parse the HTML content of the response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')
"""

def extract_competition_stage(spiel_details_text):
    """
    Helper function to extract the stage of the competition from the match report
    """
    # Define an enum for the different stages of the competition
    class CompetitionStage(Enum):
        GROUP_STAGE = 'Gruppe'
        ROUND_OF_16 = 'Achtelfinale'
        QUARTER_FINALS = 'Viertelfinale'
        SEMI_FINALS = 'Halbfinale'
        FINAL = 'Finale'

    for stage in CompetitionStage:
        if stage.value in spiel_details_text:
            return stage
    return None

def findNationalityFromProfile(profile_link):
    """
    Helper function to retrieve the (main) nationaly of a player from his profile page
    """
    # URL to the player profile
    url_base = 'https://www.transfermarkt.de'
    url = url_base + profile_link

    # Define headers to make the request look more human
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Send a GET request to the URL with the headers and store the response in a variable
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    nationalitaet = soup.find('span', text='Nationalität:')

    if nationalitaet:
        # Problem with nations with more than one word (e.g. "Vereinigte Staaten")
        # nationality = nationalitaet.find_next_sibling('span').text.split()[0]

        nationality_span = soup.find('span', text='Nationalität:').find_next_sibling('span')
        nationality = nationality_span.find_all('img')[0]['title']
        print(f"Downloaded nationality from this {profile_link} profile")
    else:
        nationality = "Unknown"
        print("ERROR: Nationality Unknown")
    return nationality

def get_starting_lineups(soup):
    """
    Give the entire soup as input. The function returns two lists, each containing 11 dictionaires of the starting players
    """
    starting_lineups = soup.find_all('div', {'class': 'large-7 columns small-12 aufstellung-vereinsseite'})
    home_starting_lineup = starting_lineups[0]
    away_starting_lineup = starting_lineups[1]

    home_players = []
    for player in home_starting_lineup.find_all('div', {'class': 'aufstellung-spieler-container'}):
        # Grab data directly from the div element
        profile_link = player.find('a')['href']
        name = player.find('a').get_text()
        top = player['style'].split(';')[0].split(':')[1].strip()
        left = player['style'].split(';')[1].split(':')[1].strip()

        # Retrieve the nationaliry of the player from his profile page
        nationality = findNationalityFromProfile(profile_link)

        home_players.append(({'name': name, 'profile_link': profile_link, 'top': top, 'left': left, 'nationality': nationality}))

    away_players = []
    for player in away_starting_lineup.find_all('div', {'class': 'aufstellung-spieler-container'}):
        # Grab data directly from the div element
        profile_link = player.find('a')['href']
        name = player.find('a').get_text()
        top = player['style'].split(';')[0].split(':')[1].strip()
        left = player['style'].split(';')[1].split(':')[1].strip()

        # Retrieve the nationaliry of the player from his profile page
        nationality = findNationalityFromProfile(profile_link)
        away_players.append(({'name': name, 'profile_link': profile_link, 'top': top, 'left': left, 'nationality': nationality}))
    
    return home_players, away_players


def get_match_data(soup, match_number):
    """
    The function takes a soup object of the entire match report site as input and returns a dictionary with the match data
    """

    # Get the match data out of the match report and store it in a dictionary
    match_data = {}

    # get the hometeam find the div element with class "sb-team sb-heim"
    div = soup.find('div', {'class': 'sb-team sb-heim'})

    # extract the link and text information from the first <a> tag inside the div element
    link = div.a['href']
    home_team_name = soup.find('div', class_='sb-team sb-heim').find('a', class_='sb-vereinslink').text

    # extract the number (like "506" for Juventus Turin) from the link using string manipulation
    home_team_number = link.split('/')[-3]

    home_team = {'name': home_team_name, 'number': home_team_number}

    # do the same for the away team
    div = soup.find('div', {'class': 'sb-team sb-gast'})

    # extract the link and text information from the first <a> tag inside the div element
    link = div.a['href']
    away_team_name = soup.find('div', class_='sb-team sb-gast').find('a', class_='sb-vereinslink').text

    # extract the number (like "506" for Juventus Turin) from the link using string manipulation
    away_team_number = link.split('/')[-3]

    away_team = {'name': away_team_name, 'number': away_team_number}

    # Get the stage of the competition out of the match report

    # Get the sb-spieldaten div element to extract the stage of competition and the result
    match_details = soup.find('div', class_='sb-spieldaten')

    if extract_competition_stage(match_details.text) != None:
        competition_stage = extract_competition_stage(match_details.text).name
    else:
        print('ERROR: Could not find the stage of the competition')

    # Get the sb-spieldaten div element to extract the stage of competition and the result
    result_panel = soup.find('div', class_='sb-endstand')

    # remove the sb-halbzeit div
    halbzeit_div = result_panel.select_one('.sb-halbzeit')
    halbzeit_div.extract()

    # Format the result string like "1:1" into a dictionary
    result_string = result_panel.text.strip()
    result_list = result_string.split(':')
    match_result = {'goals_home_team': result_list[0], 'goals_away_team': result_list[1]}

    # Store the match data in a dictionary
    match_data = {'match_number': match_number, 'home_team': home_team, 'away_team': away_team, 'competition_stage': competition_stage, 'match_result': match_result}

    # Call helper function to get the starting lineups of both teams
    home_team_starting_lineup, away_team_starting_lineup =  get_starting_lineups(soup)

    match_data['home_team']['starting_lineup'] = home_team_starting_lineup
    match_data['away_team']['starting_lineup'] = away_team_starting_lineup


    # print(match_data)
    print(f"Match data for {match_data['home_team']['name']} - {match_data['away_team']['name']} successfully extracted")

    return match_data


"""
match_data = get_match_data(soup)



# Store the match data as a json in a new folder
# The folder is named after the match number of the game
# Navigate up one level to /home/user/
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
folder_path_competition = "football-country-quiz\static\competition_data\CL2122"
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

# Call a function to generate the guessing image
generate_the_guessing_image(match_data)

generate_the_solution_image(match_data)

"""