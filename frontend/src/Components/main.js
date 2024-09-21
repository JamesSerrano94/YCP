import React from 'react';
import './main.css';

export default function MainPage() {
  return (
    <div className='container'>
      <div className='top'>
        <div className='app-name'>Yale CourseMap</div>
        <div>
          <button className='about-button'>Meet the team</button>
        </div>
      </div>

      <div className='content'>
        <div className='text-section'>
          <div className='big-title'>
            Plan your courses <br /> to align with your career path
          </div>
          <div className='description'>
          The Yale CourseMap is here to help you easily plan your courses and align them with your career goals. Using smart AI and Yale's course data, the app gives you personalized course recommendations based on what you want to achieve. No more confusion over what classes to take – this tool makes course selection simple and tailored just for you, helping you stay on track for your dream career.
          </div>
          <button className='start-button'>Start planning!</button>
        </div>

        <div className='image-section'>
          <img src='/mainPageVisual.png' alt='Visual illustration' className='main-illustration' />
        </div>
      </div>

      <div className='quotes-section'>
        <div className='quote-card' style={{ backgroundColor: 'rgba(255, 190, 186, 0.64)' }}>
          <img src='/frontquote.svg' alt='Front quote' className='quote-icon front-quote' />
          <p>
            I want to be a Machine learning Engineer specializing in the biotechnology industry. 
            Could you help me plan my course schedule for this semester?
          </p>
          <img src='/frontquote.svg' alt='Back quote' className='quote-icon back-quote' />
        </div>

        <div className='quote-card' style={{ backgroundColor: 'rgba(170, 211, 255, 0.52)' }}>
          <img src='/frontquote.svg' alt='Front quote' className='quote-icon front-quote' />
          <p>
            I'm interested in animation and visual effects. Can you help me plan my course load to 
            prepare for a career in the film industry?
          </p>
          <img src='/frontquote.svg' alt='Back quote' className='quote-icon back-quote' />
        </div>

        <div className='quote-card' style={{ backgroundColor: 'rgba(199, 199, 241, 0.68)' }}>
          <img src='/frontquote.svg' alt='Front quote' className='quote-icon front-quote' />
          <p>
            My goal is to become a data-driven financial analyst, using predictive analytics to guide 
            investment strategies. Could you help me design a course schedule?
          </p>
          <img src='/frontquote.svg' alt='Back quote' className='quote-icon back-quote' />
        </div>
      </div>
    </div>
  );
}



