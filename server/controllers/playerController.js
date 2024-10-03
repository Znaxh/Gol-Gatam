const playersArray = [
    { name: 'Player 1', 
      age : 32,
    },
    { name: 'Player 2' },
    { name: 'Player 3' },
    { name: 'Player 4' },
    { name: 'Player 5' },
    { name: 'Player 6' },
    { name: 'Player 7' },
    { name: 'Player 8' },
    { name: 'Player 9' },
    { name: 'Player 10' },
    { name: 'Player 11' },
    // Add more players as needed
];

async function getPlayer(req, res) {
    try {
        const limit = parseInt(req.query.limit) || 5;
        const offset = parseInt(req.query.offset) || 0;

        const players = playersArray.slice(offset, offset + limit);

        res.setHeader('Content-Type', 'application/json');
        res.status(200).json(players);
    } catch (error) {
        res.status(500).json({ error: 'An error occurred while fetching players.' });
    }
}

module.exports = { getPlayer };

