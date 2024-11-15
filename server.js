const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const signupRoutes = require('./routes/Signup.js');
const loginRoutes = require('./routes/Login.js');
const preferencesRoutes = require('./routes/Preferences.js');
const settingsRoutes = require('./routes/Settings');

const ATLAS_URI = 'mongodb+srv://Priyanshu:DqXO8tWPyeCmUHRU@cluster0.v9gwp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';

const app = express();

app.use(express.json());
app.use(cors());
app.use('/signup', signupRoutes);
app.use('/login', loginRoutes);
app.use('/preferences', preferencesRoutes);
app.use('/settings', settingsRoutes);
mongoose.connect(ATLAS_URI, {})
  .then(() => console.log('MongoDB connected successfully'))
  .catch(err => console.error('MongoDB connection error:', err));

app.get('/', (req, res) => {
  res.send('Server is running');});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
  console.log(`http://localhost:${PORT}`);
});