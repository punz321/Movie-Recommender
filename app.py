#frontend app 
import streamlit as st
import pandas as pd
from recom import recommended

#@st.cache_data #cache-ing the data so it doesnt load the data everytime the program runs
#def load_data():
#    movies = pd.read_csv(r"ml-100k\ml-100k\u.item", sep = "|", encoding = "latin-1")

#    return movies

#movies = load_data

#streamlit UI

st.title("(Alpha)Movie Recommender System🎬🍿")
st.write("Type a movie name to get recommendations!!")

user_input = st.text_input("Enter a movie title")

if st.button("Recommend"):
    if user_input:
        result = recommended(user_input, 5)
        st.write("### Recommendations:")
        st.dataframe(result)
    else:
        st.write("Please enter a movie title")