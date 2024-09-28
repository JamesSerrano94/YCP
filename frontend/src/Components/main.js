import React, { useRef } from "react";
import { Link } from "react-router-dom";
import './main.css';
import './courseMap.css';

export default function MainPage() {
  const courseMapRef = useRef(null);

  const scrollToCourseMap = () => {
    courseMapRef.current.scrollIntoView({ behavior: "smooth" });
  };
  return (
    <div className='container'>
      <div className='top'>
        <div className='app-name'>Yale CourseMap</div>
        <div>
          <Link to='/about-us'>
            <button className='meet-team-button'>Meet the team</button>
          </Link>
        </div>
      </div>

      <div className='content'>
        <div className='text-section'>
          <div className='big-title'>
            <div className='big-title'>
              Plan your courses to <br /> align with your <span className='highlight'>career path</span>
            </div>
          </div>
          <div className='description'>
            The Yale CourseMap is here to help you easily plan your courses and align them with your career goals. Using smart AI and Yale's course data, the app gives you personalized course recommendations based on what you want to achieve. No more confusion over what classes to take – this tool makes course selection simple and tailored just for you, helping you stay on track for your dream career.
          </div>
          <button className='start-button' onClick={scrollToCourseMap}>Start planning!</button>
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

      {/* CourseMap Section */}
      <div ref={courseMapRef} className="container">

        <main className="main-content">
          <div className="left-panel">
            <h2>Information</h2>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="major">Major</label>
              </div>
              <div className="form-group">
                <label htmlFor="semester">Semester</label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <select id="major">
                  <option>Computer Science</option>
                  <option>Mathematics</option>
                  <option>Biology</option>
                </select>
              </div>
              <div className="form-group">
                <select id="semester">
                  <option>Fall 2024</option>
                  <option>Spring 2024</option>
                </select>
              </div>
            </div>

            <h2>Course Schedule Preferences</h2>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="earliest-start-time">Earliest Start Time</label>
              </div>
              <div className="form-group">
                <label htmlFor="latest-end-time">Latest End Time</label>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <select id="earliest-start-time">
                  <option>8:00 AM</option>
                  <option>10:00 AM</option>
                  <option>12:00 PM</option>
                </select>
              </div>
              <div className="form-group">
                <select id="latest-end-time">
                  <option>6:00 PM</option>
                  <option>8:00 PM</option>
                  <option>9:00 PM</option>
                </select>
              </div>
            </div>

            <h2>Tell us more about your interests and career goals:</h2>
            <textarea className="career-goals" placeholder="e.g. I want to be a game developer..." required></textarea>
          </div>

          <div className="image-container">
            <img src="divider.svg" alt="Image Description" />
          </div>

          <div className="right-panel">
            <h2>Fulfilled Distributional Requirements</h2>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="humanities">Humanities</label>
              </div>
              <div className="form-group">
                <label htmlFor="sciences">Sciences</label>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <input type="text" id="humanities" placeholder="e.g. ENGL 114, ENGL 120" />
              </div>
              <div className="form-group">
                <input type="text" id="sciences" placeholder="e.g. CHEM 161, CHEM 162" />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="social">Social</label>
              </div>
              <div className="form-group">
                <label htmlFor="qr">QR</label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <input type="text" id="social" placeholder="e.g. KREN, L1 to L2" />
              </div>
              <div className="form-group">
                <input type="text" id="qr" placeholder="e.g. KREN, L1 to L2" />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="writing">Writing</label>
              </div>
              <div className="form-group">
                <label htmlFor="language">Language</label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <input type="text" id="writing" placeholder="e.g. KREN, L1 to L2" />
              </div>
              <div className="form-group">
                <input type="text" id="language" placeholder="e.g. KREN, L1 to L2" />
              </div>
            </div>
            <h2>Tell us more about prior courses you've taken that count for your current major</h2>
            <textarea className="prior-courses" placeholder="e.g. MATH 225, CPSC 201, CPSC 323"></textarea>

            <div className="plan-button-container">
              <button className="plan-button">Plan</button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

