

# https://www.bjjheroes.com/a-z-bjj-fighters-list

import requests
from bs4 import BeautifulSoup
import re
import csv

def get_data_from_bjj_heroes(test_ids=[]):
    url = "https://www.bjjheroes.com/a-z-bjj-fighters-list"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing the list of BJJ fighters
        table = soup.find('table')
        if table:
            # Find all the rows in the table
            rows = table.find_all('tr')

            all_fighters_df = list()
            skipped_fighters_df = list()

            # Skip the header row (index 0)
            for row in rows[1:]:
                # Extract data from each row
                columns = row.find_all('td')
                if len(columns) >= 3:  # Check if the row has at least 3 columns
                    firstname = columns[0].text.strip()
                    lastname = columns[1].text.strip()
                    nickname = columns[2].text.strip()
                    team = columns[3].text.strip()
                    skipped = 0

                    # process the fighter page ID for BJJ Heroes
                    if columns[0].find('a'):
                        fighter_url = columns[0].find('a').get('href')
                        bjjheroes_id = int(re.findall(r'\d+', fighter_url)[0])
                    else:
                        fighter_url = None
                        bjjheroes_id = None

                    print(f"Data appended to all fighters df for {firstname} {lastname}. Fighter ID: {bjjheroes_id}")

                    # Follow the link and scrape the linked page
                    # if fighter_url in ['/?p=9246', '/?p=86']:
                    # if fighter_url and (test_ids is [] or bjjheroes_id in test_ids):
                    if fighter_url:
                        linked_response = requests.get('http://bjjheroes.com' + fighter_url)
                        if linked_response.status_code == 200:
                            print(f"Getting fight data for {fighter_url}")
                            linked_soup = BeautifulSoup(linked_response.text, 'html.parser')
                            single_fighter_df = list()
                            
                            # Find the fight history table on the linked page
                            fight_history_table = linked_soup.find('table')
                            if fight_history_table:
                                # Extract and print the data from the fight history table
                                fight_history_rows = fight_history_table.find_all('tr')

                                # Check if this is a normal table or one with few details
                                if fight_history_table.get('class'):                       
                                    for fight_row in fight_history_rows:
                                        fight_columns = fight_row.find_all('td')
                                        if len(fight_columns) >= 5:
                                            match_num = fight_columns[0].text.strip()
                                            opponent_name = fight_columns[1].span.text.strip()
                                            result = fight_columns[2].text.strip()
                                            method = fight_columns[3].text.strip()
                                            competition = fight_columns[4].text.strip()
                                            weight = fight_columns[5].text.strip()
                                            stage = fight_columns[6].text.strip()
                                            year = fight_columns[7].text.strip()

                                            if fight_columns[1].find('a'):
                                                opponent_bjjheroes_id = int(re.findall(r'\d+', fight_columns[1].find('a').get('href'))[0])
                                            else:
                                                opponent_bjjheroes_id = None

                                            # convert the fight result to integer
                                            if result == 'W':
                                                result_int = 1
                                            elif result == 'D':
                                                result_int = 0.5
                                            elif result == 'L':
                                                result_int = 0 
                                            else:
                                                result_int = None,

                                            # Add match to fighter DF
                                            single_fighter_df.append({
                                                "match_num": match_num,
                                                "bjjheroes_id": bjjheroes_id,
                                                "name": f"{firstname} {lastname}",
                                                "opponent_bjjheroes_id": opponent_bjjheroes_id,
                                                "opponent_name": opponent_name,
                                                "result": result,
                                                "result_int": result_int,
                                                "method": method,
                                                "competition": competition,
                                                "weight": weight,
                                                "stage": stage,
                                                "year": year
                                            })

                                    # Export single fighter info to CSV
                                    print("Writing fighter data to CSV")
                                    filename_str = f"{bjjheroes_id}_{firstname}_{lastname}.csv"

                                    with open('./data/' + filename_str, 'w', newline='') as csvfile:
                                        writer = csv.DictWriter(csvfile, fieldnames=single_fighter_df[0].keys())
                                        
                                        # Write the header row (field names)
                                        writer.writeheader()
                                        
                                        # Write the data rows
                                        for row in single_fighter_df:
                                            writer.writerow(row)
                                else:
                                    print("This is a shorter table. Skipping")
                                    skipped = 1

                            else: 
                                print(f"Fight history table not found on the linked page: {fighter_url}")
                        else:
                            print(f"Failed to retrieve linked page: {fighter_url}")

                # Append fighter to the all_fighters_df
                all_fighters_df.append({
                    "bjjheroes_id": bjjheroes_id,
                    "first_name": firstname,
                    "last_name": lastname,
                    "full_name": f"{firstname} {lastname}",
                    "nickname": nickname,
                    "team": team,
                    "skipped": skipped
                })
            # Write All fighters to CSV
            with open('./processed/all-fighters.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_fighters_df[0].keys())
                
                # Write the header row (field names)
                writer.writeheader()
                
                # Write the data rows
                for row in all_fighters_df:
                    writer.writerow(row)
                print('all-fighters.csv file written')

        else:
            print("Table not found on the page.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    get_data_from_bjj_heroes()

