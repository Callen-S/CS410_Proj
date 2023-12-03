import pandas as pd
import requests
from io import StringIO
import os


def read_csv_files_from_github(user, repo, folder):
    # GitHub repository URL
    base_url = f'https://raw.githubusercontent.com/{user}/{repo}/main/{folder}/'

    # Fetching file names from the GitHub repository
    files = requests.get(f'https://api.github.com/repos/{user}/{repo}/contents/{folder}')
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
github_user = 'username'
github_repo = 'repository_name'
folder_name = 'folder_containing_csv_files'

# Call the function to read CSV files and store them in a dictionary
csv_data_dict = read_csv_files_from_github(github_user, github_repo, folder_name)

# Access the dictionary where keys are file names and values are Pandas DataFrames
for file_name, df in csv_data_dict.items():
    print(f"File: {file_name}\nDataFrame:\n{df}\n")