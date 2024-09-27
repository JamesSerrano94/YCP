import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Use 'Routes' instead of 'Switch'
import MainPage from './Components/main';  // Main page component
import AboutUs from './Components/AboutUs'; // About Us page component
import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          {/* Define the route for the main page */}
          <Route path="/" element={<MainPage />} /> {/* Renders MainPage on root route */}
          
          {/* Define the route for AboutUs page */}
          <Route path="/about-us" element={<AboutUs />} /> {/* Renders AboutUs when the path is /about-us */}
          
          {/* Add other routes here if needed */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
