#frontend app 
import streamlit as st
import pandas as pd
from recom import recommended

#streamlit UI
st.markdown("Movie Recommender System")
st.title("Movie Recommender System🎬🍿")
st.write("Type a movie name to get recommendations!!")

user_input = st.text_input("Enter a movie title")

if st.button("Recommend"):
    if user_input:

        clean_input = user_input.lower().strip()
        result = recommended(clean_input, 5)
        st.write("### Recommendations:")
        st.write(result)
    else:
        st.write("Please enter a movie title")