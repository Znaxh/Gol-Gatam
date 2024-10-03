import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient, errors
from fuzzywuzzy import fuzz

uri = "mongodb+srv://hackasolclient:hackasolclient123@hack-a-sol.pc9l3.mongodb.net/?retryWrites=true&w=majority&appName=hack-a-sol"

try:
    client = MongoClient(uri)
    db = client['cricket_db']
    collection = db['profiles']
except errors.ConfigurationError as e:
    print(f"ConfigurationError: {e}")
    exit(1)

df = pd.read_csv("../ml/clear_df.csv")
player_names = df['Player_name'].unique().tolist()

def find_best_match(scraped_name, csv_names):
    best_match = None
    highest_ratio = 0
    for csv_name in csv_names:
        ratio = fuzz.token_set_ratio(scraped_name, csv_name)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = csv_name
    return best_match if highest_ratio > 80 else None

for i in range(25, 1500):
    try:
        url = f'https://www.cricbuzz.com/profiles/{i}/'
        response = requests.get(url)
        print(f"Profile ID {i} status code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            profile = {}

            # Extracting Personal Information
            full_name = soup.find('h1', class_='cb-font-40').text.strip() if soup.find('h1') else None
            if not full_name:
                continue

            # Find the best match in the CSV file
            csv_name = find_best_match(full_name, player_names)
            if not csv_name:
                print(f"No match found for {full_name}. Skipping...")
                continue

            profile['Full Name'] = full_name
            profile['Player Name'] = csv_name
            profile['Born'] = soup.find('div', string='Born').find_next_sibling('div').text.strip() if soup.find('div', string='Born') else None
            profile['Birth Place'] = soup.find('div', string='Birth Place').find_next_sibling('div').text.strip() if soup.find('div', string='Birth Place') else None
            profile['Height'] = soup.find('div', string='Height').find_next_sibling('div').text.strip() if soup.find('div', string='Height') else None
            profile['Role'] = soup.find('div', string='Role').find_next_sibling('div').text.strip() if soup.find('div', string='Role') else None
            profile['Batting Style'] = soup.find('div', string='Batting Style').find_next_sibling('div').text.strip() if soup.find('div', string='Batting Style') else None
            profile['Bowling Style'] = soup.find('div', string='Bowling Style').find_next_sibling('div').text.strip() if soup.find('div', string='Bowling Style') else None
            img_tag = soup.find('img', title='profile image')
            profile['Profile Image'] = img_tag['src'] if img_tag else None

            
            icc_rankings = {}
            ranking_labels = ['Test', 'ODI', 'T20']
            ranking_values = []

            # Find all ranking values
            for ranking_value in soup.find_all('div', class_='cb-col cb-col-25 cb-plyr-rank text-right'):
                ranking_values.append(ranking_value.text.strip())

            # Split ranking values into batting and bowling
            batting_ranks = ranking_values[:3]
            bowling_ranks = ranking_values[3:]

            # Construct the ICC Rankings dictionary
            icc_rankings['Batting'] = {ranking_labels[i]: batting_ranks[i] for i in range(len(ranking_labels))}
            icc_rankings['Bowling'] = {ranking_labels[i]: bowling_ranks[i] for i in range(len(ranking_labels))}

            # Extract Career Information
            career_information = {}
            career_information_section = soup.find('div', class_='cb-col cb-col-100 cb-font-16 text-bold cb-ttl-vts')

            if career_information_section:
                teams_label = career_information_section.find_next_sibling('div', class_='cb-col cb-col-40 text-bold cb-lst-itm-sm')
                teams_value = teams_label.find_next_sibling('div', class_='cb-col cb-col-60 cb-lst-itm-sm')
                career_information['Teams'] = teams_value.text.strip() if teams_value else None
            profile['ICC Rankings'] = icc_rankings
            profile['Career Information'] = career_information

            def extract_table_data(table):
                headers = [th.text.strip() for th in table.find_all('th')[1:]]
                data = {}
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    format_name = cells[0].text.strip()
                    values = [cell.text.strip() for cell in cells[1:]]
                    data[format_name] = {
                        **dict(zip(headers, values))
                    }
                return data

            # Extract batting career summary
            batting_table = soup.find('div', string='Batting Career Summary').find_next('table') if soup.find('div', string='Batting Career Summary') else None
            if batting_table:
                batting_summary = extract_table_data(batting_table)
                profile['Batting Career Summary'] = batting_summary
            
            # Extract bowling career summary
            bowling_table = soup.find('div', string='Bowling Career Summary').find_next('table') if soup.find('div', string='Bowling Career Summary') else None
            if bowling_table:
                bowling_summary = extract_table_data(bowling_table)
                profile['Bowling Career Summary'] = bowling_summary
            
            # Extract Key Career Milestones
            career_info_div = soup.find('div', class_='cb-col cb-col-100')
            career_info = {}

            if career_info_div:
                titles = career_info_div.find_all('div', class_='cb-col cb-col-16 text-bold cb-ftr-lst')
                details = career_info_div.find_all('a', class_='cb-text-link')

                for title, detail in zip(titles, details):
                    key = title.text.strip().replace(' ', '_').lower()
                    value = detail.text.strip()
                    career_info[key] = value
                profile['Key Career Milestones'] = career_info


        try:
            collection.insert_one(profile)
            print(f"Data for profile ID {i} inserted successfully")
        except errors.PyMongoError as e:
            print(f"Data insertion failed for profile ID {i}: {e}")

    except requests.RequestException as e:
        print(f"Request failed for profile ID {i}: {e}")
    except Exception as e:
        print(f"An error occurred for profile ID {i}: {e}")
