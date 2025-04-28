# Movie Recommender 

- This recommender helps the user get the most similar moves based on the past searches and the interested genres.
The recommendation system uses two embedding files, one is title embedding which is used for direct title search and the second for larger context window which inclues the genres and the year as well. This file is used for semantic search.
- The recommender performs cosine similarity search on the query given by the user and return top 15 most similar movies similar movies in the descending order of similarity.

## Technologies used

### **MongoDb Atlas**
MongoDb is aNoSQL database for storing the data flexible JSON-like format. This makes it easier to provide the REST API architecture.
- **Role in this project**: To store all the user data such as username, password, email etc.

### **Express.js**
Express.js is a web application framework for Node.js for which is used for building the  API calls and routing of the web server.
- **Role in this project**: Backend API server for handling HTTP requests and routes.

### **React**
React is a JS library which is used for development of user interfaces of web applications.
- **Role in this project**: For building the user interfaces in the website

 ### **Node.js**
 Node.js provides a JavaScrpit runtime environment on the server side outside a web browser.
 - **Role in this project**: Server side runtime for Express.js

### **Python Flask**
Flask is a light weight Python web framework.
- **Role in this project**: The flask hosts the recommender system backend in this project.
- handles the pre-computed embedding files for search which returns the top most similar movies based on the query provided by the user.
- Uses collaborative filtering based on similar user's preferred genre.
- Get details of a specific movie from the locally stored JSON file containing the data for each movie.
## Database Used
- The Database used in this project was provided by MovieLens 32M. The data was processed to a JSON file `movies.json`. (Couldn't be included due to GitHub file size limitations)




