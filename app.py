import streamlit as st
import joblib
import tensorflow
import requests
import pandas as pd
import sklearn
from datetime import date

from get_feature import load_base_data, extract_club_features, get_match_features, find_club
'''
# Football Oracle front
'''
st.write('hello 👋 welcome to our magical and mysterious world for foodball oracle')


@st.cache_data
def get_initial_stats():
    clubs, processed_data = load_base_data()
    club_stats_dict = extract_club_features(processed_data, clubs)
    return clubs, club_stats_dict

clubs_df, stats_dict = get_initial_stats()




@st.cache_resource
def load_model():
    return joblib.load("complex_model_pipeline.pkl")

model = load_model()


st.title("⚽️ Football Oracle ")

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to input the name of the 2 teams

1. Let's ask for:
- home club name  ?
- away club name ?

'''
#home_club_name = st.text_area('home club name?',)
#away_club_name = st.text_area('away_club_name?',)

col1, col2 = st.columns(2)
with col1:
    h_search = st.text_input("search home team (e.g.: Arsenal)")
    h_results = find_club(h_search, clubs_df) if h_search else pd.DataFrame()
    if not h_results.empty:
        h_club = st.selectbox("make sure home team", h_results['name'].tolist(), key="h_select")
        h_id = h_results[h_results['name'] == h_club]['club_id'].iloc[0]

with col2:
    a_search = st.text_input("search away team (e.g: Chelsea)")
    a_results = find_club(a_search, clubs_df) if a_search else pd.DataFrame()
    if not a_results.empty:
        a_club = st.selectbox("make sure away team", a_results['name'].tolist(), key="a_select")
        a_id = a_results[a_results['name'] == a_club]['club_id'].iloc[0]

match_date = st.date_input("play time ", value=date.today())
if st.button('Here is to witness 🎈🎈🎈 the miracle of the moment !'):
    st.balloons()

if st.button("prediction"):
    try:
        # get feature model needed
        raw_features = get_match_features(stats_dict, h_id, a_id, match_date)

        # convert to  DataFrame (attention:columns name should be same with model)
        # youneed print(full_pipeline.feature_names_in_) to key
        X_input = pd.DataFrame([{
            'home_club_position': raw_features['own_position'],
            'away_club_position': raw_features['opponent_position'],
            'home_streak_2': raw_features['own_streak_2'],
            'home_streak_5': raw_features['own_streak_5'],
            'home_restday': raw_features['own_restday'],
            'away_streak_2': raw_features['opponent_streak_2'],
            'away_streak_5': raw_features['opponent_streak_5'],
            'away_restday': raw_features['opponent_restday'],
            'home_market_value': raw_features['own_market_value'],
            'away_market_value': raw_features['opponent_market_value']
        }])


        import time
        'Starting a long football divination...'

        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
        # Update the progress bar with each iteration.
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i + 1)
            time.sleep(0.1)

        '...and now we\'re done!'

        prediction = model.predict(X_input)
        st.success(f"predict result: {prediction[0]}")

        homescore =prediction[0][0]
        awayscore =prediction[0][1]
        diff = homescore -awayscore
        if diff > 0.3:
            st.write(f"🐍{h_club} win⚽️!")
        elif diff < -0.3:
            st.write(f"🐍{a_club} win⚽️")
        else:
            st.write("draw")


        st.write('🎉''home_club_position',raw_features['own_position'])
        st.write('away_club_position',raw_features['opponent_position'])
        st.write('home_streak_2',raw_features['own_streak_2'])
        st.write('home_streak_5',raw_features['own_streak_5'])
        st.write('home_restday',raw_features['own_restday'])
        st.write('away_streak_2',raw_features['opponent_streak_2'])
        st.write('away_streak_5',raw_features['opponent_streak_5'])
        st.write('away_restday',raw_features['opponent_restday'])
        st.write('home_market_value', raw_features['own_market_value'])
        st.write('away_market_value', raw_features['opponent_market_value'])


    except Exception as e:
        st.error(f"error: {e}")




'''
## Once we have these, we need look into dictionary ,
##to get the features from home club name ,away club name to
#ge
# let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

# #url = 'https://taxifare-1088852828414.europe-west1.run.app/predict'
# #url = 'https://taxifare.lewagon.ai/predict'
# ##if url == 'https://taxifare.lewagon.ai/predict':

# #   st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# ##From club_game get home id ,away id.
# e.g. define a function from 2 names of teams to get ids.

# home_club_id, away_club_id =get_id(home_club_name:str='',away_club_name:str='')

# ##From processed_data got processed features

# e.g define a seconde function from 2 ids to select the preprocessed features



# faetures X =get_features(home_club_id, away_club_id)

# X= {:
# home_club_position;
# away_club_position;
# home_streak_2
# home_streak_5
# home_restday
# away_streak_2
# away_streak_5
# away_restday
# home_market_value
# away_market_value
# }
# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
# X=pd.DataFrame({
# 'home_club_position':[16],
# 'away_club_position':[86],
# 'home_streak_2' :[3.0],
# 'home_streak_5' : [3.0],
# 'home_restday' :[6.0],
# 'away_streak_2' : [0.0],
# 'away_streak_5' : [0.0],
# 'away_restday' :[5.0],
# 'home_market_value' :[1.274111e+08],
# 'away_market_value'  :[5.309333e+07]
# })

# # if st.checkbox('Show progress bar'):
# #     import time

# #     'Starting a long computation...'

# #     # Add a placeholder
# #     latest_iteration = st.empty()
# #     bar = st.progress(0)

# #     for i in range(100):
# #         # Update the progress bar with each iteration.
# #         latest_iteration.text(f'Iteration {i+1}')
# #         bar.progress(i + 1)
# #         time.sleep(0.1)

# #     '...and now we\'re done!'

# if st.button('submit for prediction'):
#     print('submit for teams for prediction!')
#     st.write('paramter submitted 🎉')

#     #parameter ={
#     #     'home_club_position': home_club_position,
#     #     'away_club_position': away_club_position,
#     #     'home_streak_2': home_streak_2,
#     #     'home_streak_5': home_streak_5,
#     #     'home_restday': home_restday,
#     #     'away_streak_2': away_streak_2,
#     #     'away_streak_5': away_streak_5,
#     #     'away_restday': away_restday,
#     #     'home_market_value': home_market_value,
#     #     'away_market_value': away_market_value
#     #     }
#     #response = requests.get(url, params=parameter)
#     #response.json()
#     #st.write('predict score for the 2 teams', response.json())

#     #prediction = model.predict(X)
#     st.title(f'{home_club_name} ⚽️vs {away_club_name}')
#     st.write('predict score for the 2 teams', prediction)
#     homescore =prediction[0][0]
#     awayscore =prediction[0][1]
#     diff = homescore -awayscore
#     if diff > 0.3:
#         st.write(f"{home_club_name} win!")
#     elif diff < -0.3:
#         st.write(f"{away_club_name} win")
#     else:
#         st.write("draw")


#     st.write("Streamlit Map with pickup to dropout")

# else:
#     st.write('teams name for home_club and away_club not submitted 😞')

# '''
also add a function to asign the 2 teams.predict  scores
to generate a straightforward assertion for win even or lose
and round the score to integer to give it a real feeling scores

'''
