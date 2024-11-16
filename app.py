import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from video_scrapper import get_video
from recommender import model, cosine_similarity
import pickle
from LLM import get_movie_details
from recommender import recommend_movies

app = Flask(__name__)
CORS(app)

def filter_movies_by_genre(movies, genres, offset=0, limit=14):

    recommended_movies = recommend_movies(genres)
    filtered_movies = {}
    count = 0
    for movie_id, title, similarity in recommended_movies:
        if movie_id in movies:
            if count >= offset and count < offset + limit:
                filtered_movies[movie_id] = movies[movie_id]
            count += 1
            if count >= offset + limit:
                break
    return filtered_movies

def get_search_results(query, embeddings, movies, is_title_search=True, similarity_threshold=0.5):
    """Helper to get search results with confidence scores"""
    results = []
    query_embedding = model.encode(query.lower())
    
    if is_title_search:
        for movie_id, embedding in embeddings.items():
            similarity = cosine_similarity(query_embedding, embedding)
            if similarity >= similarity_threshold:
                results.append((movie_id, movies[movie_id], similarity * 1.2))
    else:
        for movie_id, data in embeddings.items():
            similarity = cosine_similarity(query_embedding, data['embedding'])
            if similarity >= similarity_threshold:
                results.append((movie_id, movies[movie_id], similarity))
                
    return results

def search_movies_by_title(movies, query, offset=0, limit=14, similarity_threshold=0.5):
    """Search using both embeddings with improved confidence scoring"""
    try:
        with open('ai/title_embeddings.pkl', 'rb') as f:
            title_embeddings = pickle.load(f)
        with open('ai/movie_combined_embeddings.pkl', 'rb') as f:
            combined_embeddings = pickle.load(f)

        query_embedding = model.encode(query.lower())
        matched_movies = []
        query_words = set(query.lower().split())
        
        # Title embeddings search
        for movie_id, embedding in title_embeddings.items():
            similarity = cosine_similarity(query_embedding, embedding)
            if similarity >= similarity_threshold:
                movie = movies[movie_id]
                title_words = set(movie['title'].lower().split())
                word_overlap = len(query_words & title_words) / len(query_words)
                adjusted_similarity = similarity * (1 + word_overlap)
                matched_movies.append((movie_id, movie, adjusted_similarity))
        
        # Combined embeddings search
        for movie_id, data in combined_embeddings.items():
            similarity = cosine_similarity(query_embedding, data['embedding'])
            if similarity >= similarity_threshold:
                if movie_id not in [m[0] for m in matched_movies]:  # Avoid duplicates
                    movie = movies[movie_id]
                    matched_movies.append((movie_id, movie, similarity))
                    print(movie, similarity)
        
        # Sort by confidence score
        matched_movies.sort(key=lambda x: x[2], reverse=True)
        
        # Apply offset and limit
        results = {}
        for movie_id, movie, _ in matched_movies[offset:offset + limit]:
            results[movie_id] = movie
            
        return results

    except Exception as e:
        print(f"Search error: {e}")
        return {}

@app.route('/')
def yes():
    return "server is running"

@app.route('/stats')
def stats():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'movies.json')
    with open(file_path, 'r') as file:
        movies = json.load(file)
        return jsonify(movies)

@app.route('/filter', methods=['POST'])
def filter_movies():
    data = request.get_json()
    genres = data.get('genre', [])
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 14))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'movies.json')
    with open(file_path, 'r') as file:
        movies = json.load(file)

    filtered_movies = filter_movies_by_genre(movies, genres, offset, limit)

    return jsonify(filtered_movies)

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 14))
    
    if not query:
        return jsonify({})
        
    with open('ai/movies.json') as f:
        movies = json.load(f)
        
    results = search_movies_by_title(movies, query, offset, limit)
    return jsonify(results)

@app.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'movies.json')
    with open(file_path, 'r') as file:
        movies = json.load(file)
        movie = movies.get(movie_id)
        if movie:
            try:
                imdb_id = str(movie['imdbId'])
                print(f'imdb_id: {imdb_id}')
                video_link = get_video(imdb_id)
                movie['video_link'] = video_link
                print(movie['video_link'])
            except Exception as e:
                print(f"Error getting video")
                movie['video_link'] = None
            return jsonify(movie)
        else:
            return jsonify({"error": "Movie not found"}), 404

@app.route('/movie_details/<movie_id>',methods=['GET'])
def movie_details(movie_id):
    movie_details = get_movie_details(movie_id)

    return movie_details

@app.route('/movie-recommendations/<movie_id>')
def get_movie_recommendations(movie_id):
    with open('ai/movies.json') as f:
        movies = json.load(f)
        
    # Get current movie's genres
    current_movie = movies.get(movie_id)
    if not current_movie:
        return jsonify({"error": "Movie not found"}), 404
        
    genres = current_movie.get('genres', [])
    
    # Get recommendations using existing filter function
    recommendations = filter_movies_by_genre(movies, genres, limit=7)
    
    # Remove the current movie from recommendations if present
    recommendations.pop(movie_id, None)
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(port=3001)