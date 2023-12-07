import pandas as pd
import requests
from io import StringIO
from search import search_data
import plotly.express as px
import streamlit as st
import os
st.set_page_config(
    page_title="Sentiment Analysis Tool",  # Title of the tab
    page_icon=":chart_with_upwards_trend:",  # Icon for the tab (optional)
)





# Your Streamlit app code goes here
st.title("Sentiment Analysis Tool - CS410")
line = st.toggle('Line or Bar Chart', value=False)
def read_csv_files_from_github(user, repo, folder):
    # GitHub repository URL
    base_url = f'https://raw.githubusercontent.com/{user}/{repo}/main/{folder}/'

    # Fetching file names from the GitHub repository
    files = requests.get(f'https://api.github.com/repos/{user}/{repo}/contents/{folder}')
    print(files.json())
    file_list = [file['name'] for file in files.json() if file['name'].endswith('.csv')]

    data_dict = {}

    # Reading CSV files and storing them in a dictionary
    for file_name in file_list:
        csv_url = base_url + file_name
        response = requests.get(csv_url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            csv_data = StringIO(content)
            df = pd.read_csv(csv_data)
            data_dict[file_name] = df

    return data_dict



# Replace 'username', 'repository_name', and 'folder_name' with your GitHub details
github_user = 'Callen-S'
github_repo = 'CS410_Proj'
folder_name = 'data'


# Call the function to read CSV files and store them in a dictionary
csv_data_dict = read_csv_files_from_github(github_user, github_repo, folder_name)

selections = st.multiselect('Select Data', csv_data_dict.keys(), default=['elon.csv'])
search_term = st.text_input('Enter a Search and eval Term', value="I think the economy is going to do well")

list_of_dfs = []
for df_key in selections:
    df = csv_data_dict[df_key]

    list_of_dfs.append(search_data(df,search_term, df_key))

df = pd.concat(list_of_dfs, ignore_index=True)
date_user_count = df.groupby('date')['user'].nunique().reset_index()

# Filtering the dates where both users have data
valid_dates = date_user_count[date_user_count['user'] == len(selections)]['date']

# Filtering the original DataFrame for rows with the valid dates
df = df[df['date'].isin(valid_dates)]

df['date'] = df['date'].astype(str)


fig = px.bar(df, x="date", y="Sentiment", color='user', hover_data='Most Relevant Text', barmode='group')
fig2 = px.bar(df, x="date", y="Relevance Score", color='user', hover_data='Most Relevant Text', barmode='group')

if line:
    fig = px.line(df, x="date", y="Sentiment", color='user', hover_data='Most Relevant Text')
    fig2 = px.line(df, x="date", y="Relevance Score", color='user', hover_data='Most Relevant Text')



fig.update_layout(autotypenumbers='convert types')
fig2.update_layout(autotypenumbers='convert types')
st.plotly_chart(fig)
st.plotly_chart(fig2)


