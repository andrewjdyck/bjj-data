
# ELO Calc

import math
import numpy as np
import pandas as pd
import csv

# Elo rating function (logistic function)
def elo_expected(A, B):
    return 1 / (1 + math.pow(10, (B - A) / 400))

def update_elo_rating(player_rating, opponent_rating, actual_result, k_factor):
    expected_result = elo_expected(player_rating, opponent_rating)
    new_rating = player_rating + k_factor * (actual_result - expected_result)
    return new_rating

def gen_fighters_df():
    # Fighters dataset
    fighters_df = list()
    with open('./processed/fighters.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            fighters_df.append(row)
    fighters_df = pd.DataFrame(fighters_df)
    fighters_df['bjjheroes_id'] = fighters_df['bjjheroes_id'].astype(int)
    return(fighters_df)

def gen_matches_df():
    # Sample match results (0 for loss, 0.5 for draw, 1 for win)
    matches = list()
    with open('./processed/elo_input_df.csv', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                matches.append(row)
    matches = pd.DataFrame(matches)
    matches['match_num'] = matches['match_num'].astype(int)
    matches['fighter1_id'] = matches['fighter1_id'].astype(int)
    matches['fighter2_id'].replace('', np.nan, inplace=True)
    matches['fighter2_id'] = matches['fighter2_id'].astype('Int32')
    return(matches)

def calc_elo(matches, fighters_df):
    # Initial Elo rating for new fighters
    INITIAL_RATING = 1500

    # K-factor for new fighters
    NEW_FIGHTER_K = 32

    # K-factor for established fighters
    ESTABLISHED_FIGHTER_K = 32
    
    fighters = {}
    for index, row in fighters_df.iterrows():
        fighters[row['bjjheroes_id']] = INITIAL_RATING

    for index, match in matches.iterrows():
        fighter1 = match["fighter1_id"]
        fighter2 = match["fighter2_id"]
        result_int = match["result_int"]

        rating1 = fighters[fighter1]

        # Need to be able to handle the situation where fighter2 does not have a bjj heroes ID
        try:
            rating2 = fighters[fighter2]
        except:
            rating2 = INITIAL_RATING

        if rating1 < 2100:
            k_factor = NEW_FIGHTER_K
        else:
            k_factor = ESTABLISHED_FIGHTER_K

        new_rating1 = update_elo_rating(rating1, rating2, float(result_int), k_factor)
        new_rating2 = update_elo_rating(rating2, rating1, 1 - float(result_int), k_factor)

        fighters[fighter1] = new_rating1
        # Need to be able to handle the situation where fighter2 does not have a bjj heroes ID
        try:
            fighters[fighter2] = new_rating2
        except:
            print('Fighter 2 does not have BJJ Heroes ID')
    return(fighters)

# update fighters_df
def update_elo(fighters_df, fighters_w_elo):
    fighters_df['elo'] = np.nan
    for index, row in fighters_df.iterrows():
        fighters_df.at[index, 'elo'] = fighters_w_elo[row['bjjheroes_id']]
    pdf = pd.DataFrame(fighters_df).sort_values(by=['elo'], ascending=False)
    return(pdf)

if __name__ == "__main__":
    fighters_df = gen_fighters_df()
    matches = gen_matches_df()
    fighters_w_elo = calc_elo(matches, fighters_df)
    fighters_elo = update_elo(fighters_df, fighters_w_elo)
    print(fighters_elo.head(20))
