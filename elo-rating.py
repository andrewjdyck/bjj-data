
# ELO Calc

import math

# Initial Elo rating for new fighters
INITIAL_RATING = 1500

# K-factor for new fighters
NEW_FIGHTER_K = 32

# K-factor for established fighters
ESTABLISHED_FIGHTER_K = 24

# Elo rating function (logistic function)
def elo_expected(A, B):
    return 1 / (1 + math.pow(10, (B - A) / 400))

def update_elo_rating(player_rating, opponent_rating, actual_result, k_factor):
    expected_result = elo_expected(player_rating, opponent_rating)
    new_rating = player_rating + k_factor * (actual_result - expected_result)
    return new_rating

# Sample data
fighters = {
    "FighterA": INITIAL_RATING,
    "FighterB": INITIAL_RATING,
    "FighterC": INITIAL_RATING
}

# Sample match results (0 for loss, 0.5 for draw, 1 for win)
matches = [
    {"fighter1": "FighterA", "fighter2": "FighterB", "result1": 1},
    {"fighter1": "FighterA", "fighter2": "FighterC", "result1": 0.5},
    {"fighter1": "FighterB", "fighter2": "FighterC", "result1": 0},
]

for match in matches:
    fighter1 = match["fighter1"]
    fighter2 = match["fighter2"]
    result1 = match["result1"]

    rating1 = fighters[fighter1]
    rating2 = fighters[fighter2]

    if rating1 < 2100:
        k_factor = NEW_FIGHTER_K
    else:
        k_factor = ESTABLISHED_FIGHTER_K

    new_rating1 = update_elo_rating(rating1, rating2, result1, k_factor)
    new_rating2 = update_elo_rating(rating2, rating1, 1 - result1, k_factor)

    fighters[fighter1] = new_rating1
    fighters[fighter2] = new_rating2

# Print updated ratings
for fighter, rating in fighters.items():
    print(f"{fighter}: Elo Rating = {rating}")

