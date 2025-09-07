#frontend app 
import streamlit as st
import requests
import pandas as pd
from recom import recommended
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY")

#streamlit UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("Movie Recommender System🎬🍿")
st.write("Type a movie name to get recommendations!!")

user_input = st.text_input("Enter a movie title")

#helper function for posters along w fetching the titles

def get_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()

    if "results" in response and response["results"]:
        poster_path = response["results"][0]["poster_path"]
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        
    print("TMDB API response:", response)
    return None 

if st.button("Recommend"):
    if user_input:
        clean_input = user_input.lower().strip()
        result = recommended(clean_input, 5)
        st.write("### Recommendations:")

        cols = st.columns(3)  # 3 posters per row

        for idx, row in result.iterrows():
            movie = row["Movie Title"]
            score = row["Similarity Score"]

            poster_url = get_poster(movie)
            col = cols[idx % 3]  # rotate between 3 columns

            with col:
                if poster_url:
                    st.image(poster_url, width=150, caption=f"{movie}\n({score}%)")
                else:
                    st.write(f"{movie} ({score}%)")
    else:
        st.write("Please enter a movie title")


