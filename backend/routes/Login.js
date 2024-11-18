// routes/Login.js
const express = require('express');
const router = express.Router();
const User = require('../models/User');
router.post('/', async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(400).json({ username: 'User does not exist' });
    }

    if (password !== user.password) {
      return res.status(400).json({ password: 'Incorrect password' });
    }

    res.json({ message: 'Login successful', userId: user._id, username: user.username, genres: user.genres });
  } catch (error) {
    console.error('Error during login:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;