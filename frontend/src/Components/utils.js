// utils.js

/**
 * Parses a string representing days into an array of day abbreviations.
 * @param {string} daysString - The string representing days (e.g., "MWF", "TTh").
 * @returns {string[]} - An array of day abbreviations (e.g., ["Mon", "Wed", "Fri"]).
 */
export const parseDays = (daysString) => {
    const days = [];
    const dayMap = { M: 'Mon', T: 'Tue', W: 'Wed', Th: 'Thu', F: 'Fri' };
    const dayOrder = ['M', 'T', 'W', 'Th', 'F'];
  
    while (daysString.length > 0) {
      if (daysString.includes('-')) {
        // Handle range like "M-F"
        const [startDay, endDay] = daysString.split('-');
        const startIndex = dayOrder.indexOf(startDay);
        const endIndex = dayOrder.indexOf(endDay);
  
        if (startIndex !== -1 && endIndex !== -1 && startIndex <= endIndex) {
          // Add all days in the range
          for (let i = startIndex; i <= endIndex; i++) {
            days.push(dayMap[dayOrder[i]]);
          }
        }
        break; // Exit the loop since the entire range is processed
      } else if (daysString.startsWith('Th')) {
        // Handle "Th" separately for Thursday
        days.push(dayMap['Th']);
        daysString = daysString.slice(2);
      } else {
        // Handle individual days
        const char = daysString[0];
        days.push(dayMap[char]);
        daysString = daysString.slice(1);
      }
    }
  
    return days;
  };
  
  /**
   * Converts a time string into minutes.
   * @param {string} timeString - The time string (e.g., "9.00a", "2.30p").
   * @returns {number} - The total minutes since midnight.
   */
  export const timeStringToMinutes = (timeString) => {
    let period = '';
    if (timeString.endsWith('a') || timeString.endsWith('p')) {
      period = timeString.slice(-1).toUpperCase();
      timeString = timeString.slice(0, -1); // Remove the 'a' or 'p' suffix
    }
  
    const [hourStr, minuteStr] = timeString.split('.');
    let hour = parseInt(hourStr, 10);
    const minute = parseInt(minuteStr, 10);
  
    if (period === 'P') {
      if (hour !== 12) hour += 12; // Convert PM times to 24-hour format
    } else if (period === 'A') {
      if (hour === 12) hour = 0; // Convert 12 AM to 0 hours
    } else {
      // No period specified, make an assumption
      if (hour >= 7 && hour <= 12) {
        // Assume AM for hours between 7 and 12
      } else {
        // Assume PM for hours between 1 and 6
        hour += 12;
      }
    }
  
    return hour * 60 + minute;
  };
  
  /**
   * Parses course times into a structured format for rendering.
   * @param {Array} courses - The array of course objects.
   * @returns {Array} - An array of course times with day, startTime, and endTime.
   */
  export const parseCourseTimes = (courses) => {
    const timePattern = /^[MTWThF]+(?:-[MTWThF]+)? \d{1,2}\.\d{2}[ap]?-?\d{1,2}\.\d{2}[ap]?$/;
  
    return courses.flatMap((course) =>
      course.time
        ? course.time.flatMap((timeString) => {
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
        : [] // Return an empty array if course.time is undefined
    );
  };
  