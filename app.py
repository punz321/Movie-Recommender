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

st.markdown(
    """
    <style>
    summary {
        color: #979d9f;
        font-weight: 500;
        cursor: pointer;
        list-style: none;
    }
    details {
        color: #979d9f;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

fallback_poster = "assets/no_poster.jpg"
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
        return{
            "poster_url": fallback_poster,
            "rating": None,
            "imdb_link": None,
            "overview": None
        }

    results = data.get("results", [])
    if not results:
        # no results at all
        return{
            "poster_url": fallback_poster,
            "rating": None,
            "imdb_link": None,
            "overview": None
        }    
    # step 2: pick the best match for the poster
    chosen = None
    if year:
        year_str = str(year)
        year_matches = [r for r in results if r.get("release_date", "").startswith(year_str)]
        if year_matches:
            chosen = year_matches[0]
    if not chosen:
    # otherwise try exact title match (title or original_title)
        for r in results:
            r_title = (r.get("title") or "").lower()
            r_original = (r.get("original_title") or "").lower()
            if r_title == title.lower() or r_original == title.lower():
                chosen = r
                break

    # fallback: use first result's poster if available
    if not chosen:  
        chosen = results[0]
        
    movie_id = chosen.get("id")
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    deets_params = {"api_key" : TMDB_API_KEY}
    try:
        details_resp = requests.get(details_url, params = deets_params, timeout = 5)
        details_resp.raise_for_status()
        details = details_resp.json()
    except Exception as e:
        print("TMDB details fetch failed!", e)
        return {
            "poster_url": fallback_poster,
            "rating": None,
            "imdb_link": None,
            "overview": None
        }
    
    poster_path = chosen.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else fallback_poster
    rating = details.get("vote_average")
    imdb_id = details.get("imdb_id")
    imdb_link = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
    overview = details.get("overview")

    return {
        "poster_url": poster_url,
        "rating" : rating,
        "imdb_link": imdb_link,
        "overview": overview
    }

def shorten_text(text, max_chars=200):
    if not text:
        return "No description available"
    return text if len(text) <= max_chars else text[:max_chars].rstrip()

if st.button("Recommend"):
    if user_input:
        clean_input = user_input.lower().strip()
        result = recommended(clean_input, 5)
        st.write("### Recommendations:")

        if isinstance(result, str):  # means "No Matches Found"
            st.warning(result)
        else:
            cols = st.columns(3)  # 3 posters per row

            for idx, row in result.iterrows():
                movie = row["Movie Title"]
                score = row["Similarity Score"]

                info = get_poster(movie)
                col = cols[idx % 3]  # rotate between 3 columns

                with col:
                    if info:
                        st.image(info["poster_url"], width=150, caption=f"{movie}\n({score}%)")
                        st.write(f"⭐ {info['rating']}/10" if info['rating'] else "⭐ N/A")
                        if info["imdb_link"]:
                            st.markdown(f"[View on IMDB]({info['imdb_link']})")
                        short_overview = shorten_text(info["overview"], max_chars=150)
                        if info["overview"]:
                            if len(info["overview"]) > 150:
                                remaining_text = info["overview"][150:]
                                st.markdown(f"<details><summary>{short_overview}</summary>{remaining_text}</details>",
                                unsafe_allow_html=True)
                            else:
                                st.caption(info["overview"])
                        else:
                            st.caption("No description available")
                    else:
                        st.write(f"{movie} ({score}%)")
    else:
        st.write("Please enter a movie title")
