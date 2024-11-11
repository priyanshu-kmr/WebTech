import React, { useContext, useState, useEffect } from 'react';
import '../../css/MainPage.css';
import MovieList from '../MainPage/MovieList.js';
import { UserContext } from '../UserContext/UserContext.js';
import IconButton from '@mui/material/IconButton';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import AccountPopup from '../MainPage/AccountPopup.js';
import { useNavigate, useLocation } from 'react-router-dom';

const MainPage = () => {
  const navigator = useNavigate();
  const location = useLocation();
  const { user } = useContext(UserContext);
  const [isPopupVisible, setPopupVisible] = useState(false);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [offset, setOffset] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!user) {
      navigator('/login');
    } else {
      const queryParams = new URLSearchParams(location.search);
      const query = queryParams.get('query') || '';
      setSearchQuery(query);
      if (query) {
        handleSearch(query);
      } else {
        fetchMovies(0, true); // Fetch movies with reset
      }
    }
  }, [user, location.search]);

  const fetchMovies = async (newOffset = 0, reset = false) => {
    setIsLoading(true);
    const userGenres = user.genres;
    const response = await fetch(`http://localhost:3001/filter?offset=${newOffset}&limit=14`, {  // Updated limit to 14
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ genre: userGenres })
    });
    const movies = await response.json();
    console.log('Fetched Movies:', movies); // Log the returned JSON from /filter

    // Convert the movies object to an array of movie objects with their ids
    const moviesArray = Object.keys(movies).map(id => ({ id, ...movies[id] }));

    // Append the new movies to the existing list or reset the list
    setRecommendedMovies(prevMovies => reset ? moviesArray : [...prevMovies, ...moviesArray]);
    setOffset(newOffset + 14);  // Updated offset increment to 14
    setIsLoading(false);
  };

  const handleSearch = async (query = searchQuery) => {
    setIsLoading(true);
    setOffset(0); // Reset offset on new search
    navigator(`?query=${query}&offset=0&limit=14`);  // Updated limit to 14
    const response = await fetch(`http://localhost:3001/search?query=${query}&offset=0&limit=14`);  // Updated limit to 14
    const searchResults = await response.json();


    const searchResultsArray = Object.keys(searchResults).map(id => ({ id, ...searchResults[id] }));

    setRecommendedMovies(searchResultsArray);
    setOffset(14);
    setIsLoading(false);
  };

  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const togglePopup = () => {
    setPopupVisible(!isPopupVisible);
  };

  const loadMoreMovies = async () => {
    setIsLoading(true);
    try {
      // Always use search if there's a query, otherwise fetch recommendations
      if (searchQuery.trim()) {
        const response = await fetch(`http://localhost:3001/search?query=${searchQuery}&offset=${offset}&limit=14`);
        const searchResults = await response.json();
        const searchResultsArray = Object.keys(searchResults).map(id => ({ id, ...searchResults[id] }));
        console.log('Search Results Response:', searchResults);
        setRecommendedMovies(prevMovies => [...prevMovies, ...searchResultsArray]);
      } else {
        await fetchMovies(offset);
      }
      setOffset(prev => prev + 14);
    } catch (error) {
      console.error('Error loading more movies:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <header className="header">
        <div>
          <input 
            type="text" 
            placeholder="Search..." 
            value={searchQuery}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
          />
          <IconButton className="search-button" disableRipple disableFocusRipple onClick={handleSearch}>
            <SearchIcon />
          </IconButton>
        </div>
        <IconButton className="icon-button" disableRipple disableFocusRipple onClick={togglePopup}>
          <AccountCircleIcon />
        </IconButton>
      </header>
      <h2>Recommended Movies</h2>

      <MovieList movies={recommendedMovies} />
      {isPopupVisible && <AccountPopup onClose={togglePopup} />}
      <div className="load-more-container">
        <button className="load-more-button" onClick={loadMoreMovies} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Load More'}
        </button>
      </div>
    </div>
  );
};

export default MainPage;