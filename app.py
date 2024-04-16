import streamlit as st
import pandas as pd

# Data stuff
elo_data = pd.read_csv('./processed/elo_output_df.csv')
elo_data['link'] = 'http://bjjheroes.com/?p=' + elo_data['bjjheroes_id'].astype('str')
dd = pd.read_csv('./processed/all-matches.csv')

def get_athletes_elo(start_rank=1, n=20):
    return(elo_data[['name', 'elo', 'link']].iloc[(start_rank-1):n])

# search container
with st.container():
    st.title('Top 20 BJJ Fighters ranked by ELO')

# middle container
with st.container():
    c2, c3 = st.columns(2)
    with c2:
        st.dataframe(get_athletes_elo(1, 20), 
            column_config={
                "link": st.column_config.LinkColumn(
                    "BJJ Heroes Profile",
                    help="Click to vist BJJ Heroes Profile",
                    max_chars=30,
                )
            },
            hide_index=True)
    c3.write('Athlete profile here')

# Bottom container
with st.container():
    st.header('More stats go here')


