// Calendar.js
import React from 'react';
import CourseDetailsTooltip from './CourseDetailsTooltip';
import { Button } from '@mui/material';

const Calendar = ({
  courseTimes,
  daysOfWeek,
  earliestTime,
  latestTime,
  getCourseColor,
  handleRemoveCourseFromCalendar,
}) => {
  return (
    <div className="calendar-body">
      <div className="time-column">
        {/* Render time slots in 30-minute intervals */}
        {Array.from({ length: (latestTime - earliestTime) / 30 }, (_, index) => {
          const totalMinutes = earliestTime + index * 30;
          const hours = Math.floor(totalMinutes / 60);
          const minutes = totalMinutes % 60;
          return (
            <div key={index} className="time-slot">
              {`${hours}:${minutes.toString().padStart(2, '0')}`}
            </div>
          );
        })}
      </div>
      <div className="days-column">
        {courseTimes.map((course, index) => {
          const startOffset =
            ((course.startTime - earliestTime) / (latestTime - earliestTime)) * 100;
          const duration =
            ((course.endTime - course.startTime) / (latestTime - earliestTime)) * 100;

          return (
            <div
              key={index}
              data-testid={`course-${course.department}-${course.courseNumber}`}
              className="calendar-event"
              style={{
                backgroundColor: getCourseColor(course),
                gridColumn: daysOfWeek.indexOf(course.day) + 1,
                top: `${startOffset}%`,
                height: `${duration}%`,
              }}
            >
              <div className="event-title">
                {course.department} {course.courseNumber}
              </div>
              <div className="event-description">{course.courseTitle}</div>
              <div
                className="delete-icon"
                onClick={() => handleRemoveCourseFromCalendar(course)}
              >
                <img src="delete.svg" alt="Delete" style={{ cursor: 'pointer' }} />
              </div>
              <CourseDetailsTooltip course={course}>
                <Button
                  size="small"
                  style={{
                    position: 'absolute',
                    bottom: '5px',
                    right: '5px',
                    fontSize: '0.7rem',
                    minWidth: 'auto',
                    padding: '2px 5px',
                    lineHeight: 1,
                  }}
                >
                  Details
                </Button>
              </CourseDetailsTooltip>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Calendar;
