// routes/SearchHistory.js
const express = require('express');
const router = express.Router();
const User = require('../models/User');

// Save search history
router.post('/search-history', async (req, res) => {
  try {
    const { userId, searchQuery } = req.body;
    await User.findByIdAndUpdate(
      userId,
      { $push: { searchHistory: searchQuery }},
      { new: true }
    );
    res.status(200).json({ message: 'Search history updated' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update search history' });
  }
});

// Get similar movies based on search history
router.get('/similar-movies/:userId', async (req, res) => {
  try {
    const user = await User.findById(req.params.userId);
    if (!user.searchHistory.length) {
      return res.json([]);
    }
    
    // Fetch similar movies based on last 5 searches
    const recentSearches = user.searchHistory.slice(-5);
    // Implementation of movie similarity logic would go here
    // For now, returning dummy data
    res.json([]);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch similar movies' });
  }
});

module.exports = router;