import requests
from bs4 import BeautifulSoup
import os
import json
"""
Get the list of participants and store their team logos in a new folder.
"""

"""
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

# Send a GET request to the URL with the headers and store the response in a variable
response = requests.get(url_matches, headers=headers)

# Parse the HTML content of the response using Beautiful Soup
soup_matches = BeautifulSoup(response.content, 'html.parser')

# Send a GET request to the URL with the headers and store the response in a variable
response = requests.get(url_participants, headers=headers)

# Parse the HTML content of the response using Beautiful Soup
soup_participants = BeautifulSoup(response.content, 'html.parser')
"""

def get_list_of_match_numbers(soup, competition):
    # Make sure the directory exists
    directory = f'data_gathering/images/{competition}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    match_numbers = []
    match_results = soup.find_all('a', class_='ergebnis-link')
    for result in match_results:
        match_numbers.append(result['id'])

    with open(f"data_gathering/images/{competition}/{competition}_match_ids.json", "w") as f:
        json.dump(match_numbers, f)

    print(f"{len(match_numbers)} match numbers stored in json")
    return match_numbers

def get_list_of_participants(soup, competition):
    # Find all instances of the "tiny_wappen" class in the HTML
    tiny_wappens = soup.find_all('img', class_='tiny_wappen')

    # Make sure the directory exists
    directory = f'data_gathering/images/{competition}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    names = []

    # Loop through each instance and extract the data
    for wappen in tiny_wappens:
        # Get the name of the team
        name = wappen['title']
        names.append(name)
    
    with open(f"data_gathering/images/{competition}/{competition}_team_names.json", "w") as f:
        json.dump(names, f)
    
    print(f"{len(names)} team names stored in json")

    return names

def download_team_logos(soup, competition):
    # Find all instances of the "tiny_wappen" class in the HTML
    tiny_wappens = soup.find_all('img', class_='tiny_wappen')

    # Make sure the directory exists
    directory = f'data_gathering/images/{competition}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Loop through each instance and extract the data
    for wappen in tiny_wappens:
        # Get the name of the team
        name = wappen['title']

        # Switch from tiny to big logo and clean the end of the link
        logo_link = wappen['src']
        logo_link = logo_link.replace("tiny", "big")
        logo_link = logo_link.split("?")[0]

        # Download the image and save it with the participant's name as the file name
        response = requests.get(logo_link)
        with open(f'data_gathering/images/{competition}/{name}.png', 'wb') as f:
            f.write(response.content)
    
    print("Done downloading logos")
    return

"""
# Make sure the directory exists
directory = f'data_gathering/images/{competition}'
if not os.path.exists(directory):
    os.makedirs(directory)

download_team_logos(soup_participants, competition)
get_list_of_participants(soup_participants, competition)
get_list_of_match_numbers(soup_matches, competition)
"""
