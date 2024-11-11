// components/MainPage/SearchHistory.js
import React from 'react';
import MovieList from '../MainPage/MovieList.js';

const SearchHistory = ({ movies, title }) => {
  if (!movies || movies.length === 0) return null;

  return (
    <div className="search-history-section">
      <h2>{title}</h2>
      <MovieList movies={movies} />
    </div>
  );
};

export default SearchHistory;