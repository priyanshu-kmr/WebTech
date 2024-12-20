
// create the user schema for the user document
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  genres: { type: [String], default: [] },
  searchHistory: { type: [String], default: [] }
});

module.exports = mongoose.model('User', userSchema);
