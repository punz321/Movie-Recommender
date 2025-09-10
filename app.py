#frontend app 
import streamlit as st
import requests
import pandas as pd
from recom import recommended
from dotenv import load_dotenv
import os
import re

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY")

#streamlit UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("Movie Recommender System🎬🍿")
st.write("Type a movie name to get recommendations!")

user_input = st.text_input("Enter a movie title")

#helper function to extract title and year for the matches

def extract_year(raw_title: str):
    s = raw_title.strip()
    # find the first occurrence of "(YYYY)""
    m = re.search(r"^(.*)\s\((\d{4})\)", s)
    if m:
        title = m.group(1).strip()
        year = int(m.group(2))
        # handle titles like "Pagemaster, The" -> "The Pagemaster" -> super annoying in the dataset
        m2 = re.match(r"^(.*),\s*(The|An|A)$", title, flags=re.IGNORECASE)
        if m2:
            title = f"{m2.group(2)} {m2.group(1)}".strip()
        return title, year
    # no year found: return original (stripped) and None for year
    return s, None

def get_poster(movie_title):
    # movie_title may already contain the year in parentheses
    title, year = extract_year(movie_title)

    # build request (use params so requests handles encoding)
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    if year:
        params["year"] = year

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("TMDB request failed:", e)
        return None

    results = data.get("results", [])
    if not results:
        # no results at all
        return None 
    
    # if we have a year, try to find a result whose release_date starts with that year
    if year:
        year_str = str(year)
        year_matches = [r for r in results if r.get("release_date", "").startswith(year_str)]
        if year_matches:
            poster_path = year_matches[0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    # otherwise try exact title match (title or original_title)
    for r in results:
        r_title = (r.get("title") or "").lower()
        r_original = (r.get("original_title") or "").lower()
        if r_title == title.lower() or r_original == title.lower():
            poster_path = r.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    # fallback: use first result's poster if available
    first_poster = results[0].get("poster_path")
    if first_poster:
        return f"https://image.tmdb.org/t/p/w500{first_poster}"

    return None

if st.button("Recommend"):
    if user_input:
        clean_input = user_input.lower().strip()
        result = recommended(clean_input, 10)
        st.write("### Recommendations:")

        if isinstance(result, str):  # means "No Matches Found"
            st.warning(result)
        else:
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


