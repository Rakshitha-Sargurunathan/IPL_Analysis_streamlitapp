import streamlit as st
import pandas as pd
import pickle

# Load the dataset
ball_by_ball = pd.read_csv('E:\VCU\MyProj\IPL\IPL_ball_by_ball_updated till 2024.csv')

# Extract the year from the 'Date' column
ball_by_ball['year'] = pd.to_datetime(ball_by_ball['Date'], dayfirst=True).dt.year

# Streamlit app
st.title('IPL Player Performance Analysis')

# User input for year and number of players
years = sorted(ball_by_ball['year'].unique())
year = st.selectbox('Select Year', years)
num_players = st.slider('Number of Top/Bottom Players', min_value=1, max_value=10, value=3)

# Filter data based on selected year
filtered_data = ball_by_ball[ball_by_ball['year'] == year]

# Top/Bottom players selection
selection = st.radio("Select Top or Bottom Players", ("Top", "Bottom"))

if selection == "Top":
    # Group by 'Striker' to find the top players
    grouped_data_batsmen = filtered_data.groupby('Striker').agg({'runs_scored': 'sum'}).reset_index()
    top_players = grouped_data_batsmen.sort_values(by='runs_scored', ascending=False).head(num_players)
    
    grouped_data_bowlers = filtered_data[filtered_data['wicket_confirmation'] == 1].groupby('Bowler').agg({'wicket_confirmation': 'count'}).reset_index()
    top_wicket_takers = grouped_data_bowlers.sort_values(by='wicket_confirmation', ascending=False).head(num_players)

    st.header(f'Top {num_players} Run-Getters for {year}')
    st.table(top_players)

    st.header(f'Top {num_players} Wicket-Takers for {year}')
    st.table(top_wicket_takers)

elif selection == "Bottom":
    # Group by 'Striker' to find the bottom players
    grouped_data_batsmen = filtered_data.groupby('Striker').agg({'runs_scored': 'sum'}).reset_index()
    bottom_players = grouped_data_batsmen.sort_values(by='runs_scored', ascending=True).head(num_players)
    
    grouped_data_bowlers = filtered_data[filtered_data['wicket_confirmation'] == 1].groupby('Bowler').agg({'wicket_confirmation': 'count'}).reset_index()
    bottom_wicket_takers = grouped_data_bowlers.sort_values(by='wicket_confirmation', ascending=True).head(num_players)

    st.header(f'Bottom {num_players} Run-Getters for {year}')
    st.table(bottom_players)

    st.header(f'Bottom {num_players} Wicket-Takers for {year}')
    st.table(bottom_wicket_takers)

#To DISPLAY Player Performance Analysis
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load player performance with salary data
player_performance_with_salary = pd.read_pickle('player_performance_with_salary.pkl')

# Streamlit app
st.title('Player Performance Analysis')

# User input for selecting a player
players = player_performance_with_salary['Striker'].unique()
selected_player = st.selectbox('Select Player', players)

# Filter data for the selected player
player_data = player_performance_with_salary[player_performance_with_salary['Striker'] == selected_player]

if not player_data.empty:
    st.subheader(f'Performance of {selected_player}')

    # Display performance data with salary
    st.write("### Performance Table")
    st.write(player_data[['year', 'total_runs', 'total_wickets']])

    # Display salary information separately
    salary = player_data['Salary'].iloc[0] if not player_data['Salary'].isna().all() else 'N/A'
    st.write(f"**Salary:** {salary}")

    # Plot trend graph
    fig, ax1 = plt.subplots()

    # Plot runs and wickets
    ax1.plot(player_data['year'], player_data['total_runs'], label='Runs Scored', marker='o', color='blue')
    ax1.plot(player_data['year'], player_data['total_wickets'], label='Wickets Taken', marker='o', color='green')

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Count')
    ax1.set_title(f'Performance Trend for {selected_player}')
    ax1.legend(loc='upper left')

    fig.tight_layout()
    st.pyplot(fig)

else:
    st.write("No performance data available for the selected player.")
