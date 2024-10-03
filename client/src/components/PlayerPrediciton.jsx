
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './PlayerPrediciton.css';


export default function PlayerPrediction() {
  const [a, setA] = useState();
  const [b, setB] = useState();
  const [oppTeam, setOppTeam] = useState('Pakistan'); // Default value for dropdown
  const [oppositionCountries, setOppositionCountries] = useState([]);
  const location = useLocation();
  const { player } = location.state;

  // List of top cricket countries
  const allCountries = [
    "Australia", "India", "Pakistan", "England", "South Africa", 
    "New Zealand", "Sri Lanka", "West Indies", "Bangladesh", "Afghanistan"
  ];

  useEffect(() => {
    // Remove the player's own country from the opposition list
    const updatedOppositionCountries = allCountries.filter(
      country => country !== player["Country"]
    );
    setOppositionCountries(updatedOppositionCountries);
  }, [player]);

  // Prediction function that only executes when oppTeam changes
  const predict = async () => {
    const response = await fetch('https://loonix.in:8443/predict', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        player: player['Player Name'],
        oppteam: oppTeam,  // Send selected opponent team
      }),
    });

    const json = await response.json();
    console.log(json);
    setA(json.run_scored);
    setB(json.strike_rate);
  };

  // Handle dropdown change and trigger prediction
  const handleOppTeamChange = (event) => {
    setOppTeam(event.target.value);
  };

  // Trigger prediction only when oppTeam changes
  useEffect(() => {
    if (oppTeam) {
      predict(); // Trigger prediction only on opponent team change
    }
  }, [oppTeam]);

  return (
    <div className="prediction-container">
      <h1>Player Prediction for {player['Full Name']}</h1>
      <p>Select the opposition team and get the performance prediction:</p>

      {/* Dropdown to select opposition team */}
      <div className="dropdown-container">
        <label htmlFor="opposition-team">Opposition Team: </label>
        <select id="opposition-team" value={oppTeam} onChange={handleOppTeamChange}>
          {oppositionCountries.map((country) => (
            <option key={country} value={country}>{country}</option>
          ))}
        </select>
      </div>

      {/* Display predicted values */}
      <div className="predicted-stats">
        <div className="predicted-value">
          <span>Predicted Score: </span>
          <strong>{a}</strong>
        </div>
        <div className="predicted-value">
          <span>Strike Rate: </span>
          <strong>{b}</strong>
        </div>
      </div>
    </div>
  );
}
