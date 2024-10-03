const express = require('express');
const router = express.Router();

async function getPlayer(req, res) {
  try {
    const db = req.db;
    const collection = db.collection('profiles');

    const limit = parseInt(req.query.limit) || 5;
    const offset = parseInt(req.query.offset) || 0;

    const players = await collection.find().skip(offset).limit(limit).toArray();

    res.setHeader('Content-Type', 'application/json');
    res.status(200).json(players);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred while fetching players.' });
  }
}

router.get('/players', getPlayer);

module.exports = router;
