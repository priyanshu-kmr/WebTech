import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def create_title_embeddings_cache(movies, cache_path='ai/title_embeddings.pkl'):
    """Create title embeddings and FAISS index"""
    if isinstance(movies, str):
        with open(movies) as f:
            movies = json.load(f)
            
    title_embeddings = {}
    embedding_list = []
    movie_ids = []
    
    for movie_id, movie_data in movies.items():
        try:
            title = movie_data.get('title', '')
            if not title:
                continue
                
            embedding = model.encode(title.lower())
            title_embeddings[movie_id] = embedding
            embedding_list.append(embedding)
            movie_ids.append(movie_id)
            
        except Exception as e:
            print(f"Error processing movie {movie_id}: {e}")
            continue

    # Create FAISS index
    embeddings_array = np.array(embedding_list).astype('float32')
    dimension = embeddings_array.shape[1]
    
    index = faiss.IndexFlatIP(dimension)  # Inner product index
    faiss.normalize_L2(embeddings_array)  # Normalize vectors
    index.add(embeddings_array)
    
    # Save everything
    with open(cache_path, 'wb') as f:
        pickle.dump({
            'embeddings': title_embeddings,
            'index': faiss.serialize_index(index),
            'movie_ids': movie_ids
        }, f)
    
    return title_embeddings, index, movie_ids

def create_movie_embeddings_cache(movies, cache_path='ai/movie_combined_embeddings.pkl'):
    """Create embeddings combining all movie fields"""
    # Load JSON if string path provided
    if isinstance(movies, str):
        with open(movies) as f:
            movies = json.load(f)

    combined_embeddings = {}
    skipped = 0
    
    for movie_id, movie_data in movies.items():
        try:
            # Skip if movie data is None or invalid
            if not movie_data or not isinstance(movie_data, dict):
                skipped += 1
                continue
                
            title = movie_data.get('title', '')
            if not title:  # Skip if no title
                skipped += 1
                continue
                
            # Extract fields with fallbacks
            title = title.lower()
            genres = ' '.join(movie_data.get('genres', [])).lower()
            year = str(movie_data.get('year', ''))
            
            # Create rich text representation
            combined_text = f"{title} {genres} {year}"
            
            # Generate embedding
            combined_embeddings[movie_id] = {
                'movie': movie_data,
                'embedding': model.encode(combined_text)
            }
            
        except Exception as e:
            print(f"Error processing movie {movie_id}: {e}")
            skipped += 1
            continue
    
    print(f"Processed {len(combined_embeddings)} movies, skipped {skipped}")
    
    with open(cache_path, 'wb') as f:
        pickle.dump(combined_embeddings, f)
    return combined_embeddings

# Load the embeddings from the pkl file
with open('ai/embeddings.pkl', 'rb') as file:
    embeddings = pickle.load(file)

# Load the title embeddings
try:
    with open('ai/title_embeddings.pkl', 'rb') as file:
        title_embeddings = pickle.load(file)
except FileNotFoundError:
    print("Title embeddings cache not found. Run create_title_embeddings_cache() first.")
    title_embeddings = {}

genres_list = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

def encode_genres(genres):
    encoding = [1 if genre in genres else 0 for genre in genres_list]
    return encoding

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def recommend_movies(input_genres):
    input_embedding = encode_genres(input_genres)
    similarities = []
    
    for movie_id, (title, embedding) in embeddings.items():
        similarity = cosine_similarity(input_embedding, embedding)
        similarities.append((movie_id, title, similarity))
    
    # Sort movies by similarity
    sorted_movies = sorted(similarities, key=lambda item: item[2], reverse=True)
    
    # Return top N recommendations
    return sorted_movies

def semantic_movie_search(query, combined_embeddings, top_k=10):
    """Search movies using semantic similarity"""
    query_embedding = model.encode(query.lower())
    
    # Calculate similarities
    similarities = []
    for movie_id, data in combined_embeddings.items():
        similarity = cosine_similarity(query_embedding, data['embedding'])
        similarities.append((movie_id, data['movie'], similarity))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_k]

def search_movies_by_title(movies, query, offset=0, limit=14):
    """Search using FAISS vector search"""
    try:
        with open('ai/title_embeddings.pkl', 'rb') as f:
            data = pickle.load(f)
            title_embeddings = data['embeddings']
            index = faiss.deserialize_index(data['index'])
            movie_ids = data['movie_ids']
        
        # Encode query
        query_vector = model.encode(query.lower())
        query_vector = query_vector.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_vector)
        
        # Search
        k = offset + limit  # Get enough results for offset
        scores, indices = index.search(query_vector, k)
        
        # Get results
        results = {}
        for idx in indices[0][offset:]:
            movie_id = movie_ids[idx]
            results[movie_id] = movies[movie_id]
            
        return results

    except Exception as e:
        print(f"Search error: {e}")
        return {}
