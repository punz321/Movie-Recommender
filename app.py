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
TMDB_API_KEY = "your_api_key_here"

def get_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    if response["results"]:
        poster_path = response["results"][0]["poster_path"]
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    return None

if st.button("Recommend"):
    if user_input:
        clean_input = user_input.lower().strip()
        result = recommended(clean_input, 5)
        st.write("### Recommendations:")

        for movie in result:
            poster_url = get_poster(movie)
        if poster_url:
            st.image(poster_url, width=150, caption=movie)
        else:
            st.write(movie)
    else:
        st.write("Please enter a movie title")


