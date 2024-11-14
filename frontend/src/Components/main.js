// MainPage.js
import React, { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import './main.css';
import './courseMap.css';
import Header from './Header';
import ContentSection from './ContentSection';
import QuotesSection from './QuotesSection';
import CourseMap from './CourseMap';
import Loading from './Loading';

export default function MainPage() {
  const courseMapRef = useRef(null);
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const apiUrl = process.env.REACT_APP_API_URL;

  // State variables for CourseMap
  const [major, setMajor] = useState("Computer Science");
  const [semester, setSemester] = useState("Spring 2025");
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
  const [pdfFile, setPdfFile] = useState(null);

  const scrollToCourseMap = () => {
    courseMapRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const handlePdfUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setPdfFile(file);
    } else {
      setPdfFile(null);
      alert("Please upload a valid PDF file");
    }
  };

  const handleStartPlanningClick = () => {
      scrollToCourseMap();
  };

  const handlePlanClick = () => {
    if (careerGoals.trim() === "") {
      alert("Please fill out your career goals.");
      return;
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

    // Set a timeout to handle long responses
    const timeoutId = setTimeout(() => {
      setIsLoading(false);
      alert("The request is taking too long. Please try again later.");
      navigate('/'); // Redirect to the main page
    }, 60000); // 1 minute timeout (60,000 ms)

    // Send POST request to the API
    fetch(`${apiUrl}/course/recommend`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        clearTimeout(timeoutId);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(responseData => {
        setIsLoading(false);
        navigate('/schedule', { state: { courses: responseData } });
      })
      .catch(error => {
        clearTimeout(timeoutId); // Clear the timeout in case of an error
        setIsLoading(false);
        console.error('There was a problem with the fetch operation:', error);
        alert("An error occurred. Please try again later.");
        navigate('/'); // Redirect to the main page on error
      });
  };

  return (
    <div className='container'>
      {isLoading && <Loading />}
      <div className={isLoading ? 'blur-content' : ''}></div>

      <Header/>
      <ContentSection
        handleButtonClick={ scrollToCourseMap}
      />
      <QuotesSection />
      {(
        <CourseMap
          courseMapRef={courseMapRef}
          major={major}
          setMajor={setMajor}
          semester={semester}
          setSemester={setSemester}
          earliestStartTime={earliestStartTime}
          setEarliestStartTime={setEarliestStartTime}
          latestEndTime={latestEndTime}
          setLatestEndTime={setLatestEndTime}
          careerGoals={careerGoals}
          setCareerGoals={setCareerGoals}
          humanities={humanities}
          setHumanities={setHumanities}
          sciences={sciences}
          setSciences={setSciences}
          social={social}
          setSocial={setSocial}
          qr={qr}
          setQr={setQr}
          writing={writing}
          setWriting={setWriting}
          language={language}
          setLanguage={setLanguage}
          priorCourses={priorCourses}
          setPriorCourses={setPriorCourses}
          handlePdfUpload={handlePdfUpload}
          pdfFile={pdfFile}
          handlePlanClick={handlePlanClick}
        />
      )}
    </div>
  );
}