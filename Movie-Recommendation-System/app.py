import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests

# Page config
st.set_page_config(page_title="IMRS", page_icon="🎬")
OMDB_API_KEY = "3b41fc18"

# Load data
df = pd.read_csv('cleanData.csv')

# Clean data
df['Votes'] = df['Votes'].astype(str).str.replace(',', '').astype(float).astype(int)
df['Rating'] = df['Rating'].astype(float)
df['Genre'] = df['Genre'].fillna('')
df['Director'] = df['Director'].fillna('')
df['Actor 1'] = df['Actor 1'].fillna('')
df['Actor 2'] = df['Actor 2'].fillna('')

# Combined features
df['combined'] = df['Genre'] + ' ' + df['Director'] + ' ' + df['Actor 1'] + ' ' + df['Actor 2']

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on movie
def get_recommendations(movie_title, cosine_sim=cosine_sim):
    if not movie_title:
        return pd.DataFrame()

    movie_title_clean = movie_title.strip().lower()
    matching_rows = df[df['Name'].str.lower() == movie_title_clean]
    if matching_rows.empty:
        matching_rows = df[df['Name'].str.lower().str.contains(movie_title_clean, na=False)]

    if matching_rows.empty:
        return pd.DataFrame()

    idx = matching_rows.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:101]  # Top 100 similar
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices].copy()

# Function to apply filters
def apply_filters(rec_df, genre, actor, director):
    if genre:
        rec_df = rec_df[rec_df['Genre'].str.contains(genre, case=False, na=False)]
    if actor:
        rec_df = rec_df[(rec_df['Actor 1'].str.contains(actor, case=False, na=False)) |
                        (rec_df['Actor 2'].str.contains(actor, case=False, na=False))]
    if director:
        rec_df = rec_df[rec_df['Director'].str.contains(director, case=False, na=False)]
    return rec_df

def _normalize_year(year):
    if year is None or pd.isna(year):
        return None
    try:
        year_int = int(float(year))
    except Exception:
        return None
    if year_int < 1800 or year_int > 2100:
        return None
    return year_int

@st.cache_data
def fetch_poster_url(title, year, api_key):
    if not title or not api_key:
        return None
    params = {'apikey': api_key, 't': title}
    valid_year = _normalize_year(year)
    if valid_year is not None:
        params['y'] = valid_year
    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        data = response.json()
        if data.get('Response') == 'True':
            poster = data.get('Poster')
            if poster and poster != 'N/A':
                return poster

        # Retry without year if the first search fails, since dataset years can be malformed
        if valid_year is not None:
            params.pop('y', None)
            response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
            data = response.json()
            if data.get('Response') == 'True':
                poster = data.get('Poster')
                if poster and poster != 'N/A':
                    return poster
    except requests.RequestException:
        return None
    return None


def get_movie_poster(row, api_key):
    poster_value = row.get('Poster') if hasattr(row, 'get') else None
    if poster_value and pd.notna(poster_value) and poster_value != '':
        return poster_value
    return fetch_poster_url(row['Name'], row.get('Year'), api_key)

# Streamlit app
st.title("IMRS")

# Session state
if 'full_rec' not in st.session_state:
    st.session_state.full_rec = pd.DataFrame()
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Inputs - all optional
movie_name = st.text_input("Movie Name (optional)")
actor = st.text_input("Actor Name (optional)")
director = st.text_input("Director Name (optional)")
genre = st.text_input("Genre (optional)")

if st.button("Get Recommendations"):
    # Get recommendations based on movie or all movies
    if movie_name:
        rec_df = get_recommendations(movie_name)
        if rec_df.empty:
            rec_df = df.copy()
    else:
        rec_df = df.copy()
    
    # Apply filters
    rec_df = apply_filters(rec_df, genre, actor, director)
    
    # Score movies
    rec_df['score'] = rec_df['Rating'] * np.log(rec_df['Votes'])
    rec_df = rec_df.sort_values('score', ascending=False).reset_index(drop=True)
    
    st.session_state.full_rec = rec_df
    st.session_state.current_index = 0

if not st.session_state.full_rec.empty:
    start = st.session_state.current_index
    end = start + 5
    current_movies = st.session_state.full_rec.iloc[start:end]
    
    if not current_movies.empty:
        st.subheader("Recommended Movies:")
        for _, row in current_movies.iterrows():
            cols = st.columns([1, 3])
            with cols[0]:
                poster_url = get_movie_poster(row, OMDB_API_KEY)
                if poster_url:
                    st.image(poster_url, width=180)
                else:
                    st.image('https://via.placeholder.com/180x270?text=No+Poster', width=180)
            with cols[1]:
                st.write(f"**Name:** {row['Name']}")
                st.write(f"**Genre:** {row['Genre']}")
                st.write(f"**Rating:** {row['Rating']}")
                st.write(f"**Director:** {row['Director']}")
                st.write(f"**Actors:** {row['Actor 1']}, {row['Actor 2']}")
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, show next 5"):
                st.session_state.current_index += 5
                st.rerun()
        with col2:
            if st.button("No, stop"):
                st.session_state.full_rec = pd.DataFrame()
                st.session_state.current_index = 0
                st.rerun()
    else:
        st.write("No more recommendations available.")