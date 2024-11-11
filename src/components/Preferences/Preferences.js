// components/Preferences/Preferences.js
import React, { useState, useContext, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from '../UserContext/UserContext.js';
import '../../css/Preferences.css';

const genresList = [
  'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western',
];

const Preferences = () => {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, setUser } = useContext(UserContext);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    if (location.state && location.state.userId) {
      setUserId(location.state.userId);
    } else if (user && user.id) {
      setUserId(user.id);
    } else {
      console.error('User ID not found');
    }
  }, [location.state, user]);

  const handleGenreClick = (genre) => {
    setSelectedGenres((prevSelected) => {
      if (prevSelected.includes(genre)) {
        return prevSelected.filter((g) => g !== genre);
      }
      return [...prevSelected, genre];
    });
  };

  const handleContinue = async () => {
    if (selectedGenres.length >= 3) {
      try {
        await axios.post('http://localhost:5000/preferences', { userId, genres: selectedGenres });
        console.log("Selected genres:", selectedGenres);
        setUser({ ...user, genres: selectedGenres });
        navigate('/main'); // Replace with your desired route
      } catch (error) {
        console.error('Error saving preferences:', error);
      }
    } else {
      alert("Please select at least three genres.");
    }
  };

  return (
    <div className="preferences-container">
      <h2>Select at least three genres of your choice</h2>
      <div className="genres">
        {genresList.map((genre) => (
          <button
            key={genre}
            className={`genre-button ${selectedGenres.includes(genre) ? 'selected' : ''}`}
            onClick={() => handleGenreClick(genre)}
          >
            {genre}
          </button>
        ))}
      </div>
      <button className="continue-button" onClick={handleContinue}>
        Continue
      </button>
    </div>
  );
};

export default Preferences;