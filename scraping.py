import requests
from bs4 import BeautifulSoup

# URL of the match report
url = 'https://www.transfermarkt.de/spielbericht/index/spielbericht/3812391'

# Define headers to make the request look more human
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Send a GET request to the URL with the headers and store the response in a variable
response = requests.get(url, headers=headers)


print(response)

# Parse the HTML content of the response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the section of the page that contains the FC Liverpool starting lineup
starting_lineup = soup.find('div', {'class': 'aufstellung-header', 'id': 'aufstellung-header-1'})

# Extract the names of the FC Liverpool players in the starting lineup
players = []
for player in starting_lineup.find_all('a', {'class': 'spielprofil_tooltip'}):
    players.append(player.get_text())

# Print the list of player names
print(players)
