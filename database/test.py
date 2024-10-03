import requests
from bs4 import BeautifulSoup

# Define the search URL
search_url = 'https://www.cricbuzz.com/search?q=travis-head&tab=player'
response = requests.get(search_url)

# Parse the HTML response
soup = BeautifulSoup(response.content, 'html.parser')

anchor_tag = soup.find('a',class_='text-hvr-underline text-black')
print(anchor_tag)
if anchor_tag:
    player_profile_link = anchor_tag['href']
    print(f"Player Profile Link: {player_profile_link}")
else:
    print("No anchor tag found inside the first 'ng-scope' div.")
