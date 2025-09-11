import pandas as pd
import numpy as np
import sklearn.metrics.pairwise as sk

data_columns = ["user_id", "item_id", "rating", "timestamp"]
user = pd.read_csv("ml-100k/u.data", sep = "\t", names = data_columns)
#print(user.head())

#Making this names column just in case my parents need a working proof of the project based 
#on the pool of movies that they have seen (in which case, i might have to change the entire dataset)

names = ["item_id", "movie_title", "release_date", "video_release_date", "IMDb_URL",
         "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
         "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
         "Romance", "Sci-Fi", "Thriller", "War", "Western"]

movies = pd.read_csv("ml-100k/u.item",
                   sep = "|",
                   encoding = "latin-1",
                   names = names
)
#print(movies.head())

merged_data = pd.merge(user, movies[["item_id", "movie_title"]], on="item_id")
#print(merged_data.head())

first_col = movies.iloc[:, [1]]
genre_col = movies.iloc[:, -18:]
full = pd.concat([first_col, genre_col], axis = 1)
#print(full.head())
#print(genre_col.head())

#Making Cosine Matrix
sim = sk.cosine_similarity(genre_col)
#print(sim)

# A neat and tidy way of having the movie titles correspond to the item_id so it's easier to fetch it later on

ttls = movies[["item_id", "movie_title"]]
#print(ttls.head())

##The basic gist of the function
#1. take the user query and find the first match in the dataset
#2. find the similarity scores for that query using the similarity matrix (exclude the first match bc its going to be the movie itself)
#3. pick top N movies that the user wants

#recommendation function
'''def recommended(title, n=5):
    norm_title = title.lower().strip()
    matches = ttls[ttls["movie_title"].str.lower().str.contains(norm_title, regex = False)]
    if matches.empty:
        return None
    idx = matches.index[0]

    sim_scores = list(enumerate(sim[idx])) #making pairs for movies and their similarity scores
    sim_scores = [x for x in sim_scores if x[0] != idx] #excluding the movie itself
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True) #ranks the movies based on their similarity scores, reverse = True bc by default it sorts in asc order
    top_n = sim_scores[:n] #takes the first n entries 
    movie_indices = [i[0] for i in top_n] #maps the indices in top_n back to movie titles
    return ttls.iloc[movie_indices] 

title = "toy story"
n = 5
'''
#recommended(title, n)

#Expanding the code a bit to make the result more user friendly
def recommended(title, n):
    norm_title = title.lower().strip()
    matches = ttls[ttls["movie_title"].str.lower().str.contains(norm_title, regex = False)]
    if matches.empty:
        return "No Matches Found"
    idx = matches.index[0]

    sim_scores = list(enumerate(sim[idx])) #making pairs for movies and their similarity scores
    sim_scores = [x for x in sim_scores if x[0] != idx] #excluding the movie itself
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True) #ranks the movies based on their similarity scores, reverse = True bc by default it sorts in asc order
    top_n = sim_scores[:n] #takes the first n entries

    res = [(ttls.iloc[i[0]].movie_title, i[1]*100) for i in top_n]
    final = pd.DataFrame(res, columns = ["Movie Title", "Similarity Score"])
    final["Similarity Score"] = final["Similarity Score"].round(2)
    print(final)
    return final

#recommended("toy story", 10)