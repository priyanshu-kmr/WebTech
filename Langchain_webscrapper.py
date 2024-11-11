# setup_embeddings.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle

def create_faiss_embeddings(movies_path='ai/movies.json', output_path='ai/faiss_embeddings.pkl'):
    # Load model and data
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    with open(movies_path) as f:
        movies = json.load(f)
    
    # Prepare data structures
    embeddings = {}
    embedding_list = []
    movie_ids = []
    skipped = 0
    
    # Create embeddings
    print("Creating embeddings...")
    for movie_id, movie_data in movies.items():
        try:
            title = movie_data.get('title')
            if not title:
                skipped += 1
                continue
                
            embedding = model.encode(title.lower())
            embeddings[movie_id] = embedding
            embedding_list.append(embedding)
            movie_ids.append(movie_id)
            
        except Exception as e:
            print(f"Error processing movie {movie_id}: {e}")
            skipped += 1
            
    print(f"Processed {len(embeddings)} movies, skipped {skipped}")
    
    # Create FAISS index
    print("Building FAISS index...")
    embedding_array = np.array(embedding_list).astype('float32')
    dimension = embedding_array.shape[1]
    
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embedding_array)
    index.add(embedding_array)
    
    # Save everything
    print("Saving embeddings...")
    with open(output_path, 'wb') as f:
        pickle.dump({
            'embeddings': embeddings,
            'index': faiss.serialize_index(index),
            'movie_ids': movie_ids
        }, f)
    
    print(f"Saved embeddings to {output_path}")
    return embeddings, index, movie_ids

if __name__ == "__main__":
    create_faiss_embeddings()