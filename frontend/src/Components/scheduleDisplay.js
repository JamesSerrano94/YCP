import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './scheduleDisplay.css';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';

const parseDays = (daysString) => {
    const days = [];
    while (daysString.length > 0) {
        if (daysString.startsWith('Th')) {
            days.push('Thu');
            daysString = daysString.slice(2);
        } else {
            const char = daysString[0];
            const dayMap = { M: 'Mon', T: 'Tue', W: 'Wed', F: 'Fri' };
            days.push(dayMap[char]);
            daysString = daysString.slice(1);
        }
    }
    return days;
};

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

// Helper function to convert time strings to minutes
const timeStringToMinutes = (timeString) => {
    const [hourStr, minuteStr] = timeString.split('.');
    let hour = parseInt(hourStr, 10);
    const minute = parseInt(minuteStr, 10);

    // Assuming classes are between 8 AM and 8 PM
    if (hour < 7) hour += 12; // Convert to PM times
    return hour * 60 + minute;
};

const parseCourseTimes = (courses) => {
    const timePattern = /^[MTWThF]+ \d{1,2}\.\d{2}-\d{1,2}\.\d{2}$/;
    return courses.flatMap((course) =>
        course.time.flatMap((timeString) => {
            if (!timePattern.test(timeString)) {
                // If it doesn't match, skip this time entry
                return [];
            }
            const [daysPart, timePart] = timeString.split(' ');
            const days = parseDays(daysPart);

            const [startTimeStr, endTimeStr] = timePart.split('-');
            const startTime = timeStringToMinutes(startTimeStr);
            const endTime = timeStringToMinutes(endTimeStr);
            return days.map((day) => ({
                ...course,
                day,
                startTime,
                endTime,
            }));
        })
    );
};

const earliestTime = 9 * 60; // 9 AM in minutes
const latestTime = 21 * 60; // 9 PM in minutes
const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

const ScheduleDisplay = () => {
    const location = useLocation();
    const coursesFromState = location.state?.courses || [];
    const colors = ['#F4A7A7', '#FFD580', '#A7D8F4', '#B8E986', '#C6A7E2', '#FFE5A7', '#E0AFAF', '#AFC0E0', '#E0E0AF', '#AFE0B4'];

    const courses = coursesFromState.map((course, index) => ({
        ...course,
        color: course.color || colors[index % colors.length],
    }));
    let courseTimes = parseCourseTimes(courses);
    courseTimes.sort((a, b) => b.courseTitle.length - a.courseTitle.length);

    return (
        <div className="calendar-container">
            <div className="calendar-header">
                <div className="time-header"></div>
                {daysOfWeek.map((day) => (
                    <div key={day} className="day-header">
                        {day}
                    </div>
                ))}
            </div>
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
                                className="calendar-event"
                                style={{
                                    backgroundColor: course.color,
                                    gridColumn: daysOfWeek.indexOf(course.day) + 1,
                                    top: `${startOffset}%`,
                                    height: `${duration}%`
                                }}
                            >
                                <div className="event-title">
                                    {course.department} {course.courseNumber}
                                </div>
                                <div className="event-description">{course.courseTitle}</div>
                                <HtmlTooltip
                                    key={index}
                                    title={
                                        <React.Fragment>
                                            <Typography color="inherit" variant="h6">
                                                {course.courseTitle}
                                            </Typography>
                                            <Typography variant="body2" sx={{ mt: 1 }}>
                                                <strong>Course time:</strong> {course.time}
                                            </Typography>
                                            <Typography variant="body2" sx={{ mt: 1 }}>
                                                <strong>Course description:</strong> {course.description}
                                            </Typography>
                                            <Typography variant="body2" sx={{ mt: 1 }}>
                                                <strong>Why do we recommend it:</strong> {course.explanation}
                                            </Typography>
                                        </React.Fragment>

                                    }
                                >
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
                                        }}>Details</Button>
                                </HtmlTooltip>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default ScheduleDisplay;
