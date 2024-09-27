import React from "react";
import { Link } from "react-router-dom"; // Import Link for routing
import './main.css'; // Import your styles

const MainPage = () => {
  return (
    <div className="main-page">
      {/* Place the button at the top-right */}
      <div className="top-right-button">
        <Link to="/about-us">
          <button className="meet-team-button">Meet the team</button>
        </Link>
      </div>
      
      {/* Add your main page content here */}
      <h1>Welcome to Yale CourseMap</h1>
    </div>
  );
};

export default MainPage;
