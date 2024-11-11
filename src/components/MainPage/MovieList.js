// components/MainPage/MovieList.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import GenreBox from './GenreBox';
import '../../css/MovieList.css';
import defaultPoster from '../../assets/image.png';

const MovieList = ({ movies }) => {
    const navigate = useNavigate();

    const handleMovieClick = (movieId) => {
        console.log('Clicked Movie ID:', movieId);
        navigate(`/movie/${movieId}`);
    };

    return (
        <div className="movie-list">
            {movies.map((movie, index) => 
            <div className="movie-container" key={index} onClick={() => handleMovieClick(movie.id)}>
                <img src={movie.url || defaultPoster} alt="movie poster" />
                <div className="overlay">
                    <div className="overlay-content">
                        <h3 className="movie-title">{movie.title}</h3>
                        <p>{movie.year}</p>
                        <div className="genre-boxes-container">
                            {movie.genres ? 
                                movie.genres.map((genre, idx) => (
                                    <GenreBox key={idx} genre={genre} />
                                ))
                                : <GenreBox genre="No genres available" />
                            }
                        </div>
                    </div>
                </div>
            </div>)}
        </div>
    )
}

export default MovieList;