
import { useLocation, useNavigate } from 'react-router-dom';
import './PlayerInfo.css';

export default function PlayerInfo() {
  const location = useLocation();
  const { player } = location.state;
  const navigate = useNavigate();

  const handlePredictionClick = () => {
    navigate('/playerPrediction', { state: { player } });
  };

  return (
    <div className="player-info-container">
      <div className="header-section">
        <div className="player-image">
          <img src={player['Profile Image']} alt={player['Full Name']} />
        </div>
        <div className="player-details">
          <h1>{player['Full Name']}</h1>
          <p><strong>Role:</strong> {player.Role}</p>
          <p><strong>Born:</strong> {player.Born}</p>
          <p><strong>Birth Place:</strong> {player['Birth Place']}</p>
          <p><strong>Height:</strong> {player.Height}</p>
          <p><strong>Batting Style:</strong> {player['Batting Style']}</p>
          <p><strong>Bowling Style:</strong> {player['Bowling Style']}</p>
        </div>
        <button className="prediction-button" onClick={handlePredictionClick}>
          Prediction
        </button>
      </div>

      <div className="career-section">
        <h2>Career Information</h2>
        <p><strong>Teams:</strong> {player['Career Information'].Teams}</p>
      </div>

      <div className="batting-summary-section">
        <h2>Batting Career Summary</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Format</th>
              <th>M</th>
              <th>Runs</th>
              <th>HS</th>
              <th>Avg</th>
              <th>SR</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(player['Batting Career Summary']).map(([format, stats]) => (
              <tr key={format}>
                <td>{format}</td>
                <td>{stats.M}</td>
                <td>{stats.Runs}</td>
                <td>{stats.HS}</td>
                <td>{stats.Avg}</td>
                <td>{stats.SR}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bowling-summary-section">
        <h2>Bowling Career Summary</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Format</th>
              <th>M</th>
              <th>Wkts</th>
              <th>BBI</th>
              <th>Avg</th>
              <th>Econ</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(player['Bowling Career Summary']).map(([format, stats]) => (
              <tr key={format}>
                <td>{format}</td>
                <td>{stats.M}</td>
                <td>{stats.Wkts}</td>
                <td>{stats.BBI}</td>
                <td>{stats.Avg}</td>
                <td>{stats.Econ}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

