// components/MoviePage/MoviePage.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../../css/MoviePage.css';

const MoviePage = () => {
    const { movieId } = useParams();
    const [movie, setMovie] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMovieDetails = async () => {
            try {
                setIsLoading(true);
                const response = await fetch(`http://localhost:3001/movie/${movieId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch movie details');
                }
                const movieDetails = await response.json();
                setMovie(movieDetails);
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchMovieDetails();
    }, [movieId]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!movie) {
        return <div>Movie not found</div>;
    }

    return (
        <div className="movie-page">
            <h1>{movie.title}</h1>
            <p>Year: {movie.year}</p>
            <p>Genres: {movie.genres.join(', ')}</p>
            <p>Average Rating: {movie.average_rating}</p>
            <p>Number of Ratings: {movie.rating_count}</p>
            
            <div className="video-container">
                {movie.video_link ? (
                    <video controls width="100%">
                        <source src={movie.video_link} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                ) : (
                    <div className="video-placeholder">
                        <p>Video preview not available</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MoviePage;