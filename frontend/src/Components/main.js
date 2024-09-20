import React from 'react';
import './main.css';

export default function MainPage() {
  return (
    <div className='container'>
        <div className='top'>
            <div className='app-name'>Yale CourseMap</div>
            <div>
                <button className='about-button'>About Us</button>
            </div>
        </div>

        <div className='big-title'>
            Your Career Planner Starts Here
        </div>
    </div>
  );
}
