
# ELO Calc

import math
import pandas as pd
import csv

# Initial Elo rating for new fighters
INITIAL_RATING = 1500

# K-factor for new fighters
NEW_FIGHTER_K = 32

# K-factor for established fighters
ESTABLISHED_FIGHTER_K = 32

# Elo rating function (logistic function)
def elo_expected(A, B):
    return 1 / (1 + math.pow(10, (B - A) / 400))

def update_elo_rating(player_rating, opponent_rating, actual_result, k_factor):
    expected_result = elo_expected(player_rating, opponent_rating)
    new_rating = player_rating + k_factor * (actual_result - expected_result)
    return new_rating

# Fighters dataset
fighters_df = list()
with open('./processed/fighters.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        # row['rating': INITIAL_RATING]
        fighters_df.append(row)


# fighters = {
#     "FighterA": INITIAL_RATING,
#     "FighterB": INITIAL_RATING,
#     "FighterC": INITIAL_RATING
# }

fighters = {}
for row in fighters_df:
    fighters[row['bjjheroes_id']] = INITIAL_RATING

# Sample match results (0 for loss, 0.5 for draw, 1 for win)
matches = list()
with open('./processed/elo_input_df.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            matches.append(row)

# matches = [
#     {"fighter1": "FighterA", "fighter2": "FighterB", "result1": 1},
#     {"fighter1": "FighterA", "fighter2": "FighterC", "result1": 0.5},
#     {"fighter1": "FighterB", "fighter2": "FighterC", "result1": 0},
# ]

for match in matches:
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

# Print updated ratings
for fighter, rating in fighters.items():
    print(f"{fighter}: Elo Rating = {rating}")

# update fighters_df
for row in fighters_df:
    row['elo'] = fighters[row['bjjheroes_id']]

pdf = pd.DataFrame(fighters_df).sort_values(by=['elo'], ascending=False)

