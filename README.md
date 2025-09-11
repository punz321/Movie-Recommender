# Movie-Recommender
a model that suggests you movies based on your interests. This is a very old and small dataset, please don't expect a huge range of movies.

### Dataset: 
MovieLens 100k - https://grouplens.org/datasets/movielens/100k/

## Day 1 
Loaded dataset in colab and did some data preprocessing

## Day 2
- Created the similarity matrix and making the recommender function 
- also trying to make a website for the same, trying streamlit for now
- tested the recommender function in colab, switching to vsc and pushing to git (finally🙏)

## Day 3
- Created the frontend skeleton using Streamlit
- Deployed the app

## Day 4
- Tried adding a new poster feature using TMDB API
- This gives either wrong posters or no posters at all
- Trying to fix this issue

## Day 5
- Poster issue is finally fixed

## Day 6
- Added a custom fallback poster for every movie whose poster isn't available
- Implemented the IMDb rating feature under each recommendation

### New Features List - (To be added)
- Add movie overview/description from TMDB along with the poster
-✅Show IMDb rating under each recommendation
- Nice hover effects for web users