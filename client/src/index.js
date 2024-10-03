import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import PlayerInfo from './components/PlayerInfo';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PlayerPrediction from './components/PlayerPrediciton'; // Prediction component


ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="playerPrediction" element={<PlayerPrediction />} />
      <Route path="/player/:id" element={<PlayerInfo />} />
    </Routes>
  </Router>,
  document.getElementById('root')
);

