import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from open_ai import calc_vibes
import matplotlib.pyplot as plt
import re

import nltk

df = pd.DataFrame(pd.read_csv('data_file3.csv'))

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters and stopwords
    text = re.sub(r'\W+', ' ', text)
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_text = [word for word in tokens if word not in stop_words]
    return filtered_text

# Preprocess text in the DataFrame
df = df.dropna(subset=['Text'])
df['Processed_Text'] = df['Text'].apply(preprocess_text)

# Function to perform BM25 search for a search term in a given text
def bm25_search(text_list, search_query):
    bm25 = BM25Okapi(text_list)
    scores = bm25.get_scores(search_query)
    return scores

# Example search term
search_term = 'economy is doing well'

# Group the DataFrame by month and perform BM25 search for each month
results = {}
for name, group in df.groupby(pd.to_datetime(df['Date']).dt.to_period('M')):
    texts = group['Processed_Text']
    relevance_scores = bm25_search(texts, preprocess_text(search_term))
    max_score_index = np.argmax(relevance_scores)  # Index of text with highest relevance
    highest_score = max(relevance_scores)  # Highest relevance score
    most_relevant_text = group.iloc[max_score_index]['Text']  # Get the text with highest relevance
    results[str(name)] = {
        'Relevance Score': highest_score,
        'Most Relevant Text': most_relevant_text
    }

# Display the most relevant text for each month
for month, result in results.items():
    print(f"Month: {month}")
    print(f"Relevance Score: {result['Relevance Score']}")
    print(f"Most Relevant Text: {result['Most Relevant Text']}")
df = pd.DataFrame(results).T
print('entering gpt')
df['Relevance_Score'] = df['Most Relevant Text'].apply(calc_vibes)
print('exit gpt')
df.to_csv('C:\\Users\\Callen\\PycharmProjects\\pythonProject3\\datacalcs.csv')
