import React, { useRef, useState } from "react";
import { Link } from "react-router-dom";
import './main.css';
import './courseMap.css';

export default function MainPage() {
  const courseMapRef = useRef(null);

  const scrollToCourseMap = () => {
    courseMapRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const [major, setMajor] = useState("Computer Science");
  const [semester, setSemester] = useState("Fall 2024");
  const [earliestStartTime, setEarliestStartTime] = useState('8:00 AM');
  const [latestEndTime, setLatestEndTime] = useState('9:00 PM');
  const [careerGoals, setCareerGoals] = useState('');
  const [humanities, setHumanities] = useState('');
  const [sciences, setSciences] = useState('');
  const [social, setSocial] = useState('');
  const [qr, setQr] = useState('');
  const [writing, setWriting] = useState('');
  const [language, setLanguage] = useState('');
  const [priorCourses, setPriorCourses] = useState('');

  const handlePlanClick = () => {
    if (careerGoals.trim() === "") {
      alert("Please fill out your career goals.");
      return; // Prevent submission if the field is empty
    }
    const data = {
      major: major,
      semester: semester,
      schedulePreferences: {
        earliestStartTime: earliestStartTime,
        latestEndTime: latestEndTime
      },
      careerGoals: careerGoals,
      fulfilledRequirements: {
        humanities: humanities.split(',').map(item => item.trim()).filter(Boolean),
        sciences: sciences.split(',').map(item => item.trim()).filter(Boolean),
        social: social.split(',').map(item => item.trim()).filter(Boolean),
        qr: qr.split(',').map(item => item.trim()).filter(Boolean),
        writing: writing.split(',').map(item => item.trim()).filter(Boolean),
        language: language.split(',').map(item => item.trim()).filter(Boolean),
        priorCourses: priorCourses.split(',').map(item => item.trim()).filter(Boolean)
      }
    };

    // Send POST request to the API
    fetch('http://localhost:8000/course/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(responseData => {
        console.log(responseData);
        // You can add further processing here, like updating state or redirecting
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };

  return (
    <div className='container'>
      <div className='top'>
        <div className='left-header'>
          <img src='/CourseMapLogo.png' alt='Yale CourseMap Logo' className='logo' />
          <div className='app-name' data-testid='app-name'>Yale CourseMap</div>
        </div>
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
            I'm interested in animation and visual effects. Can you help me plan my course load to
            prepare for a career in the film industry?
          </p>
          <img src='/frontquote.svg' alt='Back quote' className='quote-icon back-quote' />
        </div>

        <div className='quote-card' style={{ backgroundColor: 'rgba(170, 211, 255, 0.52)' }}>
          <img src='/frontquote.svg' alt='Front quote' className='quote-icon front-quote' />
          <p>
          I want to be a Software Development Engineer in the tech industry. Could you help me plan my course schedule for this semester?"
          </p>
          <img src='/frontquote.svg' alt='Back quote' className='quote-icon back-quote' />
        </div>

        <div className='quote-card' style={{ backgroundColor: 'rgba(199, 199, 241, 0.68)' }}>
          <img src='/frontquote.svg' alt='Front quote' className='quote-icon front-quote' />
          <p>
            My goal is to become a quantitative trader.
            Design a course schedule to build the necessary skills in finance, programming, and quantitative analysis.
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
                <select id="major" value={major} onChange={(e) => setMajor(e.target.value)}>
                  <option value="Computer Science">Computer Science</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="Biology">Biology</option>
                </select>
              </div>
              <div className="form-group">
                <select id="semester" value={semester} onChange={(e) => setSemester(e.target.value)}>
                  <option value="Fall 2024">Fall 2024</option>
                  <option value="Spring 2024">Spring 2024</option>
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
                <select id="earliest-start-time" value={earliestStartTime} onChange={(e) => setEarliestStartTime(e.target.value)}>
                  <option value="8:00 AM">8:00 AM</option>
                  <option value="8:00 AM">9:00 AM</option>
                  <option value="10:00 AM">10:00 AM</option>
                  <option value="10:00 AM">11:00 AM</option>
                </select>
              </div>
              <div className="form-group">
                <select id="latest-end-time" value={latestEndTime} onChange={(e) => setLatestEndTime(e.target.value)}>
                  <option value="6:00 PM">5:00 PM</option>
                  <option value="8:00 PM">6:00 PM</option>
                  <option value="8:00 PM">7:00 PM</option>
                  <option value="8:00 PM">8:00 PM</option>
                  <option value="9:00 PM">9:00 PM</option>
                </select>
              </div>
            </div>

            <h2>Tell us more about your interests and career goals:</h2>
            <textarea
              className="career-goals"
              placeholder="e.g. I want to be a game developer..."
              required
              value={careerGoals}
              onChange={(e) => setCareerGoals(e.target.value)}
            ></textarea>
          </div>

          <div className="image-container">
            <img src="divider.svg" alt="form divider" />
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
                <input
                  type="text"
                  id="humanities"
                  placeholder="e.g. ENGL 114, ENGL 120"
                  value={humanities}
                  onChange={(e) => setHumanities(e.target.value)}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  id="sciences"
                  placeholder="e.g. CHEM 161, CHEM 162"
                  value={sciences}
                  onChange={(e) => setSciences(e.target.value)}
                />
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
                <input
                  type="text"
                  id="social"
                  placeholder="e.g. ECON 110, SOCY 151"
                  value={social}
                  onChange={(e) => setSocial(e.target.value)}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  id="qr"
                  placeholder="e.g. MATH 120"
                  value={qr}
                  onChange={(e) => setQr(e.target.value)}
                />
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
                <input
                  type="text"
                  id="writing"
                  placeholder="e.g. ENGL 114, ENGL 120"
                  value={writing}
                  onChange={(e) => setWriting(e.target.value)}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  id="language"
                  placeholder="e.g. SPAN 110"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                />
              </div>
            </div>
            <h2>Tell us more about prior courses you've taken that count for your current major</h2>
            <textarea
              className="prior-courses"
              placeholder="e.g. MATH 225, CPSC 201, CPSC 323"
              value={priorCourses}
              onChange={(e) => setPriorCourses(e.target.value)}
            ></textarea>

            <div className="plan-button-container">
              <button className="plan-button" onClick={handlePlanClick}>Plan</button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}


