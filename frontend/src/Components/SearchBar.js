// SearchBar.js
import React from 'react';
import './scheduleDisplay.css'; // Ensure you have appropriate CSS

const SearchBar = ({ careerGoals, setCareerGoals, handleReplanClick }) => {
  return (
    <div className="search-bar">
      <div className="choose-more-icon">
        <img src="more.svg" alt="Choose more" />
      </div>
      <input
        type="text"
        placeholder="Refine your career goal"
        value={careerGoals}
        onChange={(e) => setCareerGoals(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleReplanClick();
        }}
      />
      <div className="search-icon" onClick={handleReplanClick}>
        <img src="plan.svg" alt="Replan" />
      </div>
    </div>
  );
};

export default SearchBar;
