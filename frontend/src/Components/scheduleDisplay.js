import React from 'react';
import './scheduleDisplay.css';

const courses = [
    { title: "KREN 110", description: "Elementary Korean I", location: "RKZ 08 - Rosenkranz Hall 08", days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], time: '10:10am-11:00am', color: '#5CB85C' },
    { title: "AMTH 431", description: "Optimization and Computation", location: "WTS A53 - Watson Center 60", days: ['Tue', 'Thu'], time: '1:15pm-2:00pm', color: '#D9534F' },
    { title: "CPSC 327", description: "Object-Oriented Programming", location: "DL 220 - Dunham Laboratory 220", days: ['Mon', 'Wed'], time: '4:00pm-5:00pm', color: '#F0AD4E' },
    { title: "CGSC 175", description: "The Mystery of Sleep", location: "LC 102 - Linsly-Chittenden Hall 102", days: ['Tue', 'Thu'], time: '4:00pm-5:00pm', color: '#9370DB' },
];

// Convert a time string like '10:10am' into total minutes since 00:00
const timeToMinutes = (time) => {
    const [hours, minutes, period] = time.match(/(\d+):(\d+)(am|pm)/).slice(1);
    let totalMinutes = (parseInt(hours) % 12) * 60 + parseInt(minutes);
    if (period === 'pm' && parseInt(hours) !== 12) totalMinutes += 12 * 60;
    return totalMinutes;
};

// Determine the earliest start time and the latest end time
const times = courses.flatMap(course => {
    const [start, end] = course.time.split('-');
    return [timeToMinutes(start), timeToMinutes(end)];
});

const earliestTime = Math.min(...times);  // Earliest course start time in minutes
const latestTime = Math.max(...times);    // Latest course end time in minutes

const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

const ScheduleDisplay = () => {
    return (
        <div className="calendar-container">
            <div className="calendar-header">
                <div className="time-header"></div>
                {daysOfWeek.map(day => (
                    <div key={day} className="day-header">{day}</div>
                ))}
            </div>
            <div className="calendar-body">
                <div className="time-column">
                    {/* Render hourly time slots */}
                    {Array.from({ length: (latestTime - earliestTime) / 60 + 1 }, (_, index) => (
                        <div key={index} className="time-slot">
                            {`${Math.floor((earliestTime + index * 60) / 60)}:00`}
                        </div>
                    ))}
                </div>
                <div className="days-column">
                    {courses.map(course => course.days.map(day => {
                        const [start, end] = course.time.split('-');
                        const startTime = timeToMinutes(start);
                        const endTime = timeToMinutes(end);
                        const startOffset = (startTime - earliestTime) / (latestTime - earliestTime) * 100; // Calculate position from the top
                        const duration = (endTime - startTime) / (latestTime - earliestTime) * 100; // Calculate height of the event block
                        return (
                            <div 
                                key={`${course.title}-${day}`} 
                                className="calendar-event" 
                                style={{ 
                                    backgroundColor: course.color, 
                                    gridColumn: daysOfWeek.indexOf(day) + 2,
                                    top: `${startOffset}%`, 
                                    height: `${duration}%`,
                                    position: 'absolute', // Ensure that events are positioned correctly
                                }}
                            >
                                <div className="event-title">{course.title}</div>
                                <div className="event-description">{course.description}</div>
                                <div className="event-location">{course.location}</div>
                                <div className="event-time">{course.time}</div>
                            </div>
                        );
                    }))}
                </div>
            </div>
        </div>
    );
};

export default ScheduleDisplay;
