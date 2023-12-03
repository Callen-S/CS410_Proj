import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from open_ai import calc_vibes
import matplotlib.pyplot as plt
import re
import nltk



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


# Function to perform BM25 search for a search term in a given text
def bm25_search(text_list, search_query):
    bm25 = BM25Okapi(text_list)
    scores = bm25.get_scores(search_query)
    return scores

def search_data(df, search_term, user_person):
    # Preprocess text in the DataFrame
    df = df.dropna(subset=['Text'])
    df['Processed_Text'] = df['Text'].apply(preprocess_text)
    # Example search term


    # Group the DataFrame by month and perform BM25 search for each month
    results = {}
    for name, group in df.groupby(pd.to_datetime(df['Time']).dt.to_period('M')):
        texts = group['Processed_Text']
        relevance_scores = bm25_search(texts, preprocess_text(search_term))
        max_score_index = np.argmax(relevance_scores)  # Index of text with highest relevance
        highest_score = max(relevance_scores)  # Highest relevance score
        most_relevant_text = group.iloc[max_score_index]['Text']  # Get the text with highest relevance
        results[str(name)] = {
            'Relevance Score': highest_score,
            'Most Relevant Text': most_relevant_text,
            'date': name,
            'user':user_person
        }

    # Display the most relevant text for each month
    df = pd.DataFrame(results).T
    print('enter')
    df['Sentiment'] = df['Most Relevant Text'].apply(calc_vibes, term=search_term)

    return df