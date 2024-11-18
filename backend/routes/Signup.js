// routes/Signup.js

const express = require('express');
const router = express.Router();
const User = require('../models/User');

// Signup route
router.post('/', async (req, res) => {
  const { username, email, password } = req.body;

  try {
    // Check if the username already exists
    const userByUsername = await User.findOne({ username });
    // Check if the email already exists
    const userByEmail = await User.findOne({ email });

    if (userByUsername || userByEmail) {
      return res.status(400).json({
        ...(userByUsername && { username: 'Username is already taken' }),
        ...(userByEmail && { email: 'Email is already linked to another account' })
      });
    }


    // Create a new user
    const newUser = new User({ username, email, password: password });
    await newUser.save();

    // Include the user ID in the response
    res.status(201).json({ message: 'User created successfully', user: { _id: newUser._id } });
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

router.post('/preferences', async (req, res) => {
  const { userId, genres } = req.body;

  try {
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    user.genres = genres;
    await user.save();

    res.status(200).json({ message: 'Preferences saved successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;