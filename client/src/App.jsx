import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import PlayerInfo from './components/PlayerInfo';
import './App.css';

export default function App() {
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const fetchPlayers = async () => {
    setLoading(true);
    try {
      const response = await fetch(`https://loonix.in:8443/api/players?limit=100&offset=${offset}`);
      const data = await response.json();

      const playersWithUniqueIds = data.map((player, index) => ({
        ...player,
        uniqueId: `${player._id}-${offset + index}`,
      }));

      setPlayers(prevPlayers => [...prevPlayers, ...playersWithUniqueIds]);
      setOffset(prevOffset => prevOffset + 5);
    } catch (error) {
      console.error('Error fetching players:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPlayers();
  }, []);

  // Handle player search
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    const filtered = players.filter(player =>
      player['Full Name'].toLowerCase().includes(e.target.value.toLowerCase())
    );
    setFilteredPlayers(filtered);
  };

  const handlePlayerClick = (player) => {
    navigate(`/player/${player._id}`, { state: { player } });
  };

  return (
    <div className="container">
      <div className="inner-container">
        <h1 className="header">Cricket Players</h1>

        {/* Search bar */}
        <div className="search-bar-container">
          <input
            type="text"
            className="search-input"
            placeholder="Search by player name"
            value={searchQuery}
            onChange={handleSearch}
          />
        </div>

        <div className="grid">
          {/* Use filteredPlayers if search query exists, otherwise display all */}
          {(searchQuery ? filteredPlayers : players).map(player => (
            <div key={player.uniqueId} className="card" onClick={() => handlePlayerClick(player)}>
              <div className="card-content">
                <div className="card-header">
                  <img
                    src={player['Profile Image']}
                    alt={player['Full Name']}
                    className="avatar"
                  />
                  <h2 className="player-name">{player['Full Name']}</h2>
                </div>
                <p className="player-info"><strong>Role:</strong> {player.Role}</p>
                <p className="player-info"><strong>Born:</strong> {player.Born}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="load-more-container">
          <button
            onClick={fetchPlayers}
            disabled={loading}
            className={`button ${loading ? 'disabled-button' : ''}`}
          >
            {loading ? 'Loading...' : 'Load More'}
          </button>
        </div>
      </div>
    </div>
  );
}

