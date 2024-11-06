import React, { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import './main.css';
import './courseMap.css';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';

export default function MainPage() {
  const courseMapRef = useRef(null);
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const scrollToCourseMap = () => {
    courseMapRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const [major, setMajor] = useState("Computer Science");
  const [semester, setSemester] = useState("Fall 2024");
  const [earliestStartTime, setEarliestStartTime] = useState('8:00 AM');
  const [latestEndTime, setLatestEndTime] = useState('9:00 PM');
  const [careerGoals, setCareerGoals] = useState('');
  const [humanities, setHumanities] = useState(0);
  const [sciences, setSciences] = useState(0);
  const [social, setSocial] = useState(0);
  const [qr, setQr] = useState(0);
  const [writing, setWriting] = useState(0);
  const [language, setLanguage] = useState('');
  const [priorCourses, setPriorCourses] = useState('');

  const HtmlTooltip = styled(({ className, children, ...props }) => (
    <Tooltip {...props} classes={{ popper: className }} arrow>
      {children}
    </Tooltip>
  ))(({ theme }) => ({
    // Styles applied to the popper element (outermost element)
    [`& .${tooltipClasses.tooltip}`]: {
      backgroundColor: '#ffffff',
      color: '#333333',
      maxWidth: 500,
      border: '1px solid #dadde9',
      boxShadow: '0px 2px 10px rgba(0, 0, 0, 0.2)',
      padding: '10px',
    },
    // Styles for the arrow
    [`& .${tooltipClasses.arrow}`]: {
      color: '#ffffff',
    },
  }));

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
        priorCourses: priorCourses.split(',').map(item => item.trim()).filter(Boolean)
      },
      needDistributionals: {
        humanities,
        sciences,
        social,
        qr,
        writing,
        language: language,
      }
    };
    localStorage.setItem('coursePlan', JSON.stringify(data));
    setIsLoading(true);

    const apiUrl = process.env.REACT_APP_API_URL;
    // Send POST request to the API
    fetch(`${apiUrl}/course/recommend`, {
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
        navigate('/schedule', { state: { courses: responseData } });
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };
  const Loading = () => (
    <div className="loading-overlay">
      <div className="loading-spinner"></div>
      <p>Loading your personalized schedule...</p>
    </div>
  );

  return (
    <div className='container'>
      {isLoading && <Loading />}
      <div className={isLoading ? 'blur-content' : ''}></div>
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
            I want to be a Software Development Engineer in the tech industry. Could you help me plan my course schedule for this semester?
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
                  <option value="African American Studies">African American Studies</option>
                  <option value="African Studies">African Studies</option>
                  <option value="American Studies">American Studies</option>
                  <option value="Anthropology">Anthropology</option>
                  <option value="Applied Mathematics">Applied Mathematics</option>
                  <option value="Applied Physics">Applied Physics</option>
                  <option value="Archaeological Studies">Archaeological Studies</option>
                  <option value="Architecture">Architecture</option>
                  <option value="Art">Art</option>
                  <option value="Astronomy">Astronomy</option>
                  <option value="Astrophysics">Astrophysics</option>
                  <option value="Biomedical Engineering">Biomedical Engineering</option>
                  <option value="Chemical Engineering">Chemical Engineering</option>
                  <option value="Chemistry">Chemistry</option>
                  <option value="Classical Civilization">Classical Civilization</option>
                  <option value="Classics">Classics</option>
                  <option value="Cognitive Science">Cognitive Science</option>
                  <option value="Comparative Literature">Comparative Literature</option>
                  <option value="Computer Science">Computer Science</option>
                  <option value="Computer Science and Economics">Computer Science and Economics</option>
                  <option value="Computer Science and Mathematics">Computer Science and Mathematics</option>
                  <option value="Computer Science and Psychology">Computer Science and Psychology</option>
                  <option value="Computing and Linguistics">Computing and Linguistics</option>
                  <option value="Computing and the Arts">Computing and the Arts</option>
                  <option value="Earth and Planetary Sciences">Earth and Planetary Sciences</option>
                  <option value="East Asian Languages and Literatures">East Asian Languages and Literatures</option>
                  <option value="East Asian Studies">East Asian Studies</option>
                  <option value="Ecology and Evolutionary Biology">Ecology and Evolutionary Biology</option>
                  <option value="Economics">Economics</option>
                  <option value="Economics and Mathematics">Economics and Mathematics</option>
                  <option value="Electrical Engineering">Electrical Engineering</option>
                  <option value="Electrical Engineering and Computer Science">Electrical Engineering and Computer Science</option>
                  <option value="Engineering Sciences">Engineering Sciences</option>
                  <option value="English">English</option>
                  <option value="Environmental Engineering">Environmental Engineering</option>
                  <option value="Environmental Studies">Environmental Studies</option>
                  <option value="Ethics, Politics, and Economics">Ethics, Politics, and Economics</option>
                  <option value="Ethnicity, Race, and Migration">Ethnicity, Race, and Migration</option>
                  <option value="Film and Media Studies">Film and Media Studies</option>
                  <option value="French">French</option>
                  <option value="German Studies">German Studies</option>
                  <option value="Global Affairs">Global Affairs</option>
                  <option value="Greek">Greek</option>
                  <option value="History">History</option>
                  <option value="History of Art">History of Art</option>
                  <option value="History of Science, Medicine, and Public Health">History of Science, Medicine, and Public Health</option>
                  <option value="Humanities">Humanities</option>
                  <option value="Italian Studies">Italian Studies</option>
                  <option value="Jewish Studies">Jewish Studies</option>
                  <option value="Latin American Studies">Latin American Studies</option>
                  <option value="Linguistics">Linguistics</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="Mathematics and Philosophy">Mathematics and Philosophy</option>
                  <option value="Mathematics and Physics">Mathematics and Physics</option>
                  <option value="Mechanical Engineering">Mechanical Engineering</option>
                  <option value="Modern Middle East Studies">Modern Middle East Studies</option>
                  <option value="Molecular Biophysics and Biochemistry">Molecular Biophysics and Biochemistry</option>
                  <option value="Molecular, Cellular, and Developmental Biology">Molecular, Cellular, and Developmental Biology</option>
                  <option value="Music">Music</option>
                  <option value="Near Eastern Languages and Civilizations">Near Eastern Languages and Civilizations</option>
                  <option value="Neuroscience">Neuroscience</option>
                  <option value="Philosophy">Philosophy</option>
                  <option value="Physics">Physics</option>
                  <option value="Physics and Geosciences">Physics and Geosciences</option>
                  <option value="Physics and Philosophy">Physics and Philosophy</option>
                  <option value="Political Science">Political Science</option>
                  <option value="Portuguese">Portuguese</option>
                  <option value="Psychology">Psychology</option>
                  <option value="Religious Studies">Religious Studies</option>
                  <option value="Russian">Russian</option>
                  <option value="Russian, East European, and Eurasian Studies">Russian, East European, and Eurasian Studies</option>
                  <option value="Sociology">Sociology</option>
                  <option value="South Asian Studies">South Asian Studies</option>
                  <option value="Spanish">Spanish</option>
                  <option value="Special Divisional Major">Special Divisional Major</option>
                  <option value="Statistics and Data Science">Statistics and Data Science</option>
                  <option value="Theater, Dance, and Performance Studies">Theater, Dance, and Performance Studies</option>
                  <option value="Urban Studies">Urban Studies</option>
                  <option value="Women’s, Gender, and Sexuality Studies">Women’s, Gender, and Sexuality Studies</option>
                </select>
              </div>
              <div className="form-group">
                <select id="semester" value={semester} onChange={(e) => setSemester(e.target.value)}>
                  <option value="Fall 2024">Fall 2024</option>
                  <option value="Spring 2025">Spring 2025</option>
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
                  <option value="9:00 AM">9:00 AM</option>
                  <option value="10:00 AM">10:00 AM</option>
                  <option value="11:00 AM">11:00 AM</option>
                </select>
              </div>
              <div className="form-group">
                <select id="latest-end-time" value={latestEndTime} onChange={(e) => setLatestEndTime(e.target.value)}>
                  <option value="5:00 PM">5:00 PM</option>
                  <option value="6:00 PM">6:00 PM</option>
                  <option value="7:00 PM">7:00 PM</option>
                  <option value="8:00 PM">8:00 PM</option>
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
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <h2>Distributional Requirements For This Semester</h2>
              <HtmlTooltip
                title={
                  <React.Fragment>
                    <Typography color="inherit">
                      <strong>Instructions:</strong>
                      <br />
                      - Enter the number of distributional courses you want to take in each category (integer values only).
                      For example, if you want to take 3 Humanities courses, enter "3".
                      <br />
                      - For language, specify the language type and proficiency level (text only).
                    </Typography>

                  </React.Fragment>
                }
              >
    <img
      src="/alert-circle.svg" // Path from the public folder
      alt="Info icon"
      style={{
        color: 'red',
        marginLeft: 8,
        width: 20,
        height: 20,
        cursor: 'pointer',
        transform: 'translateY(3px)' // Adjust vertical alignment
      }}
    />
              </HtmlTooltip>
            </div>

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
                  type="number"
                  id="humanities"
                  value={humanities}
                  onChange={(e) => setHumanities(Number(e.target.value))}
                />
              </div>
              <div className="form-group">
                <input
                  type="number"
                  id="sciences"
                  value={sciences}
                  onChange={(e) => setSciences(Number(e.target.value))}
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
                  type="number"
                  id="social"
                  value={social}
                  onChange={(e) => setSocial(Number(e.target.value))}
                />
              </div>
              <div className="form-group">
                <input
                  type="number"
                  id="qr"
                  value={qr}
                  onChange={(e) => setQr(Number(e.target.value))}
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
                  type="number"
                  id="writing"
                  value={writing}
                  onChange={(e) => setWriting(Number(e.target.value))}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  id="language"
                  placeholder="e.g. L3 SPAN"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                />
              </div>
            </div>
            <h2>Tell us more about prior courses you've taken that count for your current major</h2>
            <textarea
              className="prior-courses"
              placeholder="e.g. MATH 225, CPSC 201, CPSC 223, CPSC 323"
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


