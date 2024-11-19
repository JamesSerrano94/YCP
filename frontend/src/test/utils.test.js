import { parseDays, timeStringToMinutes, parseCourseTimes } from '../Components/utils.js';

describe('Utils functions', () => {
  describe('parseDays', () => {
    test('parses individual days correctly', () => {
      expect(parseDays('MWF')).toEqual(['Mon', 'Wed', 'Fri']);
      expect(parseDays('TTh')).toEqual(['Tue', 'Thu']);
    });

    test('parses a range of days correctly', () => {
      expect(parseDays('M-F')).toEqual(['Mon', 'Tue', 'Wed', 'Thu', 'Fri']);
    });

    test('handles mixed ranges and individual days', () => {
      expect(parseDays('F')).toEqual(['Fri']);
    });

    test('returns an empty array for an empty string', () => {
      expect(parseDays('')).toEqual([]);
    });
  });

  describe('timeStringToMinutes', () => {
    test('converts AM times correctly', () => {
      expect(timeStringToMinutes('9.00a')).toBe(9 * 60); // 540 minutes
      expect(timeStringToMinutes('12.30a')).toBe(30); // 12:30 AM is 30 minutes past midnight
    });

    test('converts PM times correctly', () => {
      expect(timeStringToMinutes('3.45p')).toBe(15 * 60 + 45); // 945 minutes
      expect(timeStringToMinutes('12.15p')).toBe(12 * 60 + 15); // 12:15 PM is 735 minutes
    });

    test('handles times without a period (assumes AM or PM)', () => {
      expect(timeStringToMinutes('7.30')).toBe(7 * 60 + 30); // Assumes 7:30 AM
      expect(timeStringToMinutes('3.45')).toBe(15 * 60 + 45); // Assumes 3:45 PM
    });

    test('returns NaN for invalid inputs', () => {
      expect(timeStringToMinutes('invalid')).toBeNaN();
      expect(timeStringToMinutes('')).toBeNaN();
    });
  });

  describe('parseCourseTimes', () => {
    const mockCourses = [];

    test('parses course times correctly', () => {
      const parsedTimes = parseCourseTimes(mockCourses);
      expect(parsedTimes).toEqual([]);
    });

    test('returns an empty array for courses with no time', () => {
      const courses = [
        { courseTitle: 'No Time Course', time: [] },
      ];
      expect(parseCourseTimes(courses)).toEqual([]);
    });

    test('skips invalid time strings', () => {
      const courses = [
        { courseTitle: 'Invalid Time Course', time: ['invalid time'] },
      ];
      expect(parseCourseTimes(courses)).toEqual([]);
    });
  });
});
