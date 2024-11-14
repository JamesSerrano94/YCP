// RecommendationList.js
import React from 'react';
import CourseDetailsTooltip from './CourseDetailsTooltip';
import { Button } from '@mui/material';

const RecommendationList = ({ recommendationCourses, handleAddCourseToCalendar }) => {
  return (
    <div className="recommendation-list">
      {recommendationCourses.map((course, index) => (
        <div
          key={index}
          data-testid={`recommendation-${course.department}-${course.courseNumber}`}
          className="recommendation-card"
        >
          <div className="recommendation-content">
            <div className="event-title">
              {course.department} {course.courseNumber}
            </div>
            <div className="event-description">{course.courseTitle}</div>
            <div className="event-description">{course.time}</div>
            <CourseDetailsTooltip course={course}>
              <Button
                size="small"
                style={{
                  bottom: '5px',
                  right: '5px',
                  fontSize: '0.7rem',
                  minWidth: 'auto',
                  padding: '2px 5px',
                  lineHeight: 1,
                  textAlign: 'right',
                }}
              >
                Details
              </Button>
            </CourseDetailsTooltip>
          </div>
          <div className="recommendation-action">
            <img
              src="add.svg"
              alt="Add"
              onClick={() => handleAddCourseToCalendar(course)}
              style={{ cursor: 'pointer' }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export default RecommendationList;
