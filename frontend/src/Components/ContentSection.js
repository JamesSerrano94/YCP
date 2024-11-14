// ContentSection.js
import React from 'react';

function ContentSection({ isAuthenticated, handleButtonClick }) {
  return (
    <div className='content'>
      <div className='text-section'>
        <div className='big-title'>
          Plan your courses to <br /> align with your <span className='highlight'>career path</span>
        </div>
        <div className='description'>
          The Yale CourseMap is here to help you easily plan your courses and align them with your career goals. Using smart AI and Yale's course data, the app gives you personalized course recommendations based on what you want to achieve. No more confusion over what classes to take – this tool makes course selection simple and tailored just for you, helping you stay on track for your dream career.
        </div>
        <button className='start-button' onClick={handleButtonClick}>
          {isAuthenticated ? 'Start planning!' : 'Yale CAS Sign In'}
        </button>
      </div>

      <div className='image-section'>
        <img src='/mainPageVisual.png' alt='Visual illustration' className='main-illustration' />
      </div>
    </div>
  );
}

export default ContentSection;
