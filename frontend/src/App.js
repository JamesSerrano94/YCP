import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './Components/main';  // Import your MainPage component
import AboutUs from './Components/AboutUs'; // Import the AboutUs component
import ScheduleDisplay from './Components/scheduleDisplay';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} /> {/* MainPage on root route */}
        <Route path="/about-us" element={<AboutUs />} /> {/* AboutUs on /about-us */}
        <Route path="/schedule-display" element={<ScheduleDisplay />} /> {/* AboutUs on /about-us */}
      </Routes>
    </Router>
  );
}

export default App;
