
import os
import csv
import pandas as pd


# Clean data

# I want to create a master list of matches

def load_data(file_path):
    datalist = list()
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    bjjheroes_id, firstname, lastname = file_name.split('-')
    with open(file_path, newline='') as csvfile:
        # Create a CSV reader
        csv_reader = csv.DictReader(csvfile)

        # Iterate through the rows in the CSV file
        for row in csv_reader:
            row['bjjheroes_id'] = bjjheroes_id
            row['name'] = f"{firstname} {lastname}"
            datalist.append(row)
    return(datalist)

# dd = load_data('./data/84-Alexandre-Ribeiro.csv')

# Specify the directory path
directory_path = "./data"

# List all files in the directory
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
files.pop(files.index('all-fighters.csv'))
files.pop(files.index('all-matches.csv'))

# Load all data
df = list()
for file in files:
    print(f"./data/{file}")
    df += load_data(f"./data/{file}")


# files that give me grief
# 12599-Brianna-Ste-Marie
# 7502-Paul-Ardila-Ibarra
# 7686-Sergio-Ardila-Ibarra
# 9014-Levi-Jones-Leary
# 7002-Shane-Hill-Taylor
# 9515-Seif-Eddine-Houmine

with open('./data/all-matches.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=df[0].keys())
            
    # Write the header row (field names)
    writer.writeheader()
    
    # Write the data rows
    for row in df:
        writer.writerow(row)

def create_agg_match_df(raw_match_df):
    dd = pd.DataFrame(raw_match_df).sort_values(by=['match_num'])

    # Group the data by the 'Category' column
    # Select the first observation within each group
    fo = dd.groupby('match_num', as_index=False).first()[
        ["match_num", "bjjheroes_id", "name", "opponent_bjjheroes_id", "opponent_name", "result_int"]
    ]
    fo.columns = ["match_num", "fighter1_id", "fighter1_name", "fighter2_id", "fighter2_name", "result_int"]
    return(fo)
    
tt = create_agg_match_df(df)
print(tt.loc[tt['match_num'] == '11340'])

# write the elo input df to csv
tt.to_csv('./processed/elo_input_df.csv', index=False)


## Create the fighters dataset
def create_fighter_ratings_df(raw_match_df):
    ddd = pd.DataFrame(raw_match_df).sort_values(by=['match_num'])

    # Group the data by the 'Category' column
    # Select the first observation within each group
    ttt = ddd.groupby('match_num', as_index=False).first()[
        ["match_num", "bjjheroes_id", "name", "opponent_bjjheroes_id", "opponent_name", "result_int"]
    ]
    # fo.columns = ["match_num", "fighter1_id", "fighter1_name", "fighter2_id", "fighter2_name", "result_int"]
    tttt = ttt.groupby('bjjheroes_id', as_index=False).first()[
        ['bjjheroes_id', 'name']
    ]
    return(tttt)
fighter_df = create_fighter_ratings_df(df)
fighter_df.to_csv('./processed/fighters.csv', index=False)