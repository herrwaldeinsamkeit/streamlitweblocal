import pandas as pd
import datetime
import streamlit as st
import joblib
import requests
import pandas as pd
from datetime import date

def load_base_data():
    #make sure all clubs.csv and processed_data.csv are in the same folder of streanlit
    clubs = pd.read_csv("clubs.csv")
    processed_data = pd.read_csv("processed_data.csv")
    processed_data['date'] = pd.to_datetime(processed_data['date'])
    return clubs, processed_data

def find_club(search_string,clubs):
    search_string_lower = search_string.lower()

    # Filter the clubs DataFrame for matches in 'club_code' or 'name'
    matching_clubs = clubs[
        clubs['club_code'].str.lower().str.contains(search_string_lower, na=False)|
        clubs['name'].str.lower().str.contains(search_string_lower, na=False)
    ]
    return matching_clubs[['club_id', 'name']]




def extract_club_features(df,clubs):
    club_features = {}
    # Ensure the dataframe is sorted by club and date for correct 'last game' and 'most recent' calculations
    df_sorted = df.sort_values(by=['club_id', 'date']).copy()

    for club_id in df_sorted['club_id'].unique():
        club_df = df_sorted[df_sorted['club_id'] == club_id]

        # Get club name
        club_name = clubs[clubs['club_id'] == club_id]['name'].iloc[0] if club_id in clubs['club_id'].values else None

        # Last game date
        last_game_date = club_df['date'].max()

        # Market value (average of last 3 games)
        # Get the last 3 market values, handling cases where there are fewer than 3 games
        market_values = club_df.tail(3)['own_market_value']
        avg_market_value = market_values.mean() if not market_values.empty else None

        # Most recent position
        most_recent_position = club_df['own_position'].iloc[-1] if not club_df.empty else None

        # Most recent streak_2
        most_recent_streak_2 = club_df['own_streak_2'].iloc[-1] if not club_df.empty else None

        # Most recent streak_5
        most_recent_streak_5 = club_df['own_streak_5'].iloc[-1] if not club_df.empty else None

        club_features[club_id] = {
            'club_name': club_name,
            'last_game': last_game_date,
            'market_value_avg_last_3': avg_market_value,
            'position_most_recent': most_recent_position,
            'streak_2_most_recent': most_recent_streak_2,
            'streak_5_most_recent': most_recent_streak_5
        }
    return club_features

# Extract and display club features
# club_stats_dict = extract_club_features(processed_data)

# club_stats_df = pd.DataFrame.from_dict(club_stats_dict, orient='index')


def get_match_features(club_stats_dict, club_id_1, club_id_2, input_date):
    match_features = {}

    # Convert input_date to datetime if it's not already
    if not isinstance(input_date, (pd.Timestamp, datetime.datetime)): # Corrected to datetime.datetime
        input_date = pd.to_datetime(input_date)

    # Get features for club 1 (home team)
    club_1_data = club_stats_dict.get(club_id_1)
    if club_1_data is None:
        raise ValueError(f"Club ID {club_id_1} not found in club_stats_dict")

    # Get features for club 2 (away team)
    club_2_data = club_stats_dict.get(club_id_2)
    if club_2_data is None:
        raise ValueError(f"Club ID {club_id_2} not found in club_stats_dict")

    # Calculate rest days
    own_restday = (input_date - club_1_data['last_game']).days
    opponent_restday = (input_date - club_2_data['last_game']).days

    match_features['is_home'] = 1 # As requested, home team perspective
    match_features['own_restday'] = own_restday
    match_features['opponent_restday'] = opponent_restday
    match_features['own_market_value'] = club_1_data['market_value_avg_last_3']
    match_features['opponent_market_value'] = club_2_data['market_value_avg_last_3']
    match_features['own_position'] = club_1_data['position_most_recent']
    match_features['opponent_position'] = club_2_data['position_most_recent']
    match_features['own_streak_2'] = club_1_data['streak_2_most_recent']
    match_features['opponent_streak_2'] = club_2_data['streak_2_most_recent']
    match_features['own_streak_5'] = club_1_data['streak_5_most_recent']
    match_features['opponent_streak_5'] = club_2_data['streak_5_most_recent']

    return match_features
