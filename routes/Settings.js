// routes/Settings.js
const express = require('express');
const router = express.Router();
const User = require('../models/User');

router.get('/:userId', async (req, res) => {
    try {
        const user = await User.findById(req.params.userId);
        if (!user) return res.status(404).json({ error: 'User not found' });
        res.json({ username: user.username, email: user.email });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

router.put('/update/:userId', async (req, res) => {
    const { username, email } = req.body;
    const userId = req.params.userId;

    try {
        // Check if username or email already exists
        const existingUsername = await User.findOne({ username, _id: { $ne: userId } });
        if (existingUsername) {
            return res.status(400).json({ username: 'Username already taken' });
        }

        const existingEmail = await User.findOne({ email, _id: { $ne: userId } });
        if (existingEmail) {
            return res.status(400).json({ email: 'Email already linked to another account' });
        }

        // Update user
        const updatedUser = await User.findByIdAndUpdate(
            userId,
            { username, email },
            { new: true }
        );

        res.json({ user: updatedUser });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

router.post('/verify-password/:userId', async (req, res) => {
    try {
        const user = await User.findById(req.params.userId);
        if (user.password === req.body.password) {
            res.json({ verified: true });
        } else {
            res.status(400).json({ error: 'Incorrect password' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

router.delete('/delete/:userId', async (req, res) => {
    try {
        await User.findByIdAndDelete(req.params.userId);
        res.json({ message: 'Account deleted successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;