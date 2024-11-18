# Movie Recommender 

- This recommender helps the user get the most similar moves based on the past searches and the interested genres.
The recommendation system uses two embedding files, one is title embedding which is used for direct title search and the second for larger context window which inclues the genres and the year as well. This file is used for semantic search.
- The recommender performs cosine similarity search on the query given by the user and return top 15 most similar movies similar movies in the descending order of similarity.



