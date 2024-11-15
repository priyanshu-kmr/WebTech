// routes/Preferences.js
const express = require('express');
const router = express.Router();
const User = require('../models/User.js');

router.post('/', async (req, res) => {
  const { userId, genres } = req.body;

  try {
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    user.genres = genres;
    await user.save();

    res.status(200).json({ message: 'Preferences updated successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});

module.exports = router;