import google.generativeai as genai
import json
import os

# Set your API key
genai.configure(api_key='AIzaSyDot_92mp4Zd4iz1NhTV9ULDfAkoNZQ0_g')
model = genai.GenerativeModel("gemini-1.5-flash")
def get_movie_details(movie_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'movies.json')
    
    with open(file_path, 'r') as file:
        movies = json.load(file)
        movie = movies.get(movie_id)
        
        if not movie:
            return {"error": "Movie not found"}
        
        title = movie['title']
        
        prompt = f"""
        Provide the following details for the movie "{title}" The description should not be more than 100 words". Just fill the fields without code fences.
        {{
            "title": "{title}",
            "description": "<desc>",
            "directors": ["<director1>", "<director2>", ..],
            "actors": ["<actor1>", "<actor2>", "<actor3>", ..]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        if response_text.startswith('```json') and response_text.endswith('```'):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith('```') and response_text.endswith('```'):
            response_text = response_text[3:-3].strip()

        try:
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            return {"Error": "Could not parse response as JSON"}



