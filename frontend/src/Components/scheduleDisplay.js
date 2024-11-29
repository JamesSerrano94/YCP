// scheduleDisplay.js
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import './scheduleDisplay.css';
import LoadingOverlay from './Loading';
import SearchBar from './SearchBar';
import RecommendationList from './RecommendationList';
import Calendar from './Calendar';
import { parseCourseTimes} from './utils';

const earliestTime = 8 * 60; // 8 AM in minutes
const latestTime = 22 * 60; // 10 PM in minutes
const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

const ScheduleDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [calendarCourses, setCalendarCourses] = useState(location.state?.courses?.[1] || []);
  const [recommendationCourses, setRecommendationCourses] = useState(() => {
    const courses = location.state?.courses || [];
    const firstList = Array.isArray(courses[0]) ? courses[0] : [];
    const secondList = Array.isArray(courses[2]) ? courses[2] : [];
    return [...firstList, ...secondList]; // Combine the two lists
  });

  const colors = [
    '#F4A7A7',
    '#FFD580',
    '#A7D8F4',
    '#B8E986',
    '#C6A7E2',
    '#FFE5A7',
    '#E0AFAF',
    '#AFC0E0',
    '#E0E0AF',
    '#AFE0B4',
  ];
  const [careerGoals, setCareerGoals] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const apiUrl = process.env.REACT_APP_API_URL;

  const getCourseColor = (course) => {
    const courseId = `${course.department}${course.courseNumber}`;
    let hash = 0;
    for (let i = 0; i < courseId.length; i++) {
      hash = courseId.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash % colors.length);
    return colors[index];
  };


  useEffect(() => {
    // Load stored data from local storage when the component mounts
    const storedData = JSON.parse(localStorage.getItem('coursePlan'));
    if (storedData) {
      setCareerGoals(storedData.careerGoals || '');
      // Load other form fields if needed
    }
  }, []);

  const handleReplanClick = () => {
    const storedData = JSON.parse(localStorage.getItem('coursePlan'));
    if (storedData && !isSubmitting) {
      setIsSubmitting(true);
      const updatedData = {
        ...storedData,
        careerGoals, // Update career goals with the current value
      };

      setIsLoading(true);

      // Set a timeout to handle long responses
      const timeoutId = setTimeout(() => {
        setIsLoading(false);
        setIsSubmitting(false);
        alert('The request is taking too long. Please try again later.');
        navigate('/'); // Redirect to the main page
      }, 300000); // 5 minute timeout

      fetch(`${apiUrl}/course/recommend`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
      })
        .then((response) => {
          clearTimeout(timeoutId);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((responseData) => {
          const combinedRecommendations = [
            ...new Set([
              ...(responseData[0] || []),
              ...(responseData[1] || []),
              ...(responseData[2] || []),
            ]),
          ];

          const newRecommendations = combinedRecommendations.filter((recCourse) => {
            return !calendarCourses.some((calCourse) => areCoursesEqual(calCourse, recCourse));
          });
          setRecommendationCourses(newRecommendations);
          setIsLoading(false);
          setIsSubmitting(false);
        })
        .catch((error) => {
          clearTimeout(timeoutId);
          setIsLoading(false);
          setIsSubmitting(false);
          console.error('There was a problem with the fetch operation:', error);
          alert('An error occurred. Please try again later.');
          navigate('/'); // Redirect to the main page on error
        });
    }
  };

  const areCoursesEqual = (courseA, courseB) => {
    return courseA.courseTitle === courseB.courseTitle;
  };

  const handleAddCourseToCalendar = (course) => {
    setRecommendationCourses((prev) => prev.filter((c) => !areCoursesEqual(c, course)));
    setCalendarCourses((prev) => [...prev, course]);
  };

  const handleRemoveCourseFromCalendar = (course) => {
    setCalendarCourses((prev) => prev.filter((c) => !areCoursesEqual(c, course)));
    setRecommendationCourses((prev) => [...prev, course]);
  };

  let courseTimes = parseCourseTimes(calendarCourses);
  courseTimes.sort((a, b) => b.courseTitle.length - a.courseTitle.length);

  return (
    <div className="schedule-container">
      {isLoading && <LoadingOverlay />}
      <div className={isLoading ? 'blur-content' : ''}></div>
      <div className="calendar-container">
        <div className="back-arrow-container2">
          <Link to="/">
            <button className="back-arrow-button" aria-label="Go back">
              <img src="/back-arrow.svg" alt="Back Arrow" />
            </button>
          </Link>
        </div>
        <div className="calendar-header">
          <div className="time-header"></div>
          {daysOfWeek.map((day) => (
            <div key={day} className="day-header">
              {day}
            </div>
          ))}
        </div>
        <SearchBar
          careerGoals={careerGoals}
          setCareerGoals={setCareerGoals}
          handleReplanClick={handleReplanClick}
        />
        <Calendar
          courseTimes={courseTimes}
          daysOfWeek={daysOfWeek}
          earliestTime={earliestTime}
          latestTime={latestTime}
          getCourseColor={getCourseColor}
          handleRemoveCourseFromCalendar={handleRemoveCourseFromCalendar}
        />
      </div>
      <div className="recommendation-container">
        <div className="feedback">
          <a
            href="https://docs.google.com/forms/d/e/1FAIpQLScyonigzkcblq3AOgAyFVAhEJ87NOuMpH9WN-I3yXpcTI2Zyg/viewform"
            target="_blank"
            rel="noopener noreferrer"
          >
            Give us feedback!
          </a>
        </div>
        <div className="recommendations-title">More Recommendations</div>
        <RecommendationList
          recommendationCourses={recommendationCourses}
          handleAddCourseToCalendar={handleAddCourseToCalendar}
        />
      </div>
    </div>
  );
};

export default ScheduleDisplay;