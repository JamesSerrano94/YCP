// Header.js
import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div className='top'>
      <div className='left-header'>
        <img src='/CourseMapLogo.png' alt='Yale CourseMap Logo' className='logo' />
        <div className='app-name' data-testid='app-name'>Yale CourseMap</div>
      </div>
      <div className="button-container">
        <Link to='/about-us'>
          <button className='meet-team-button'>Meet the team</button>
        </Link>
      </div>
    </div>
  );
}

export default Header;

