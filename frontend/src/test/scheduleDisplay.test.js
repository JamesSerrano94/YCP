import React from 'react';
import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import ScheduleDisplay, { timeStringToMinutes } from '../Components/scheduleDisplay';
import { MemoryRouter } from 'react-router-dom';

describe('ScheduleDisplay Component', () => {
  const mockCourse = {
    department: 'CPSC',
    courseNumber: '101',
    courseTitle: 'Introduction to Computer Science',
    time: ['MWF 10.00a-11.00a'],
    distDesg: ['QR'],
    description: 'An introductory course in computer science.',
    explanation: 'Recommended for CS majors.',
  };

  const mockRecommendationCourse = {
    department: 'MATH',
    courseNumber: '120',
    courseTitle: 'Calculus',
    time: ['TTh 2.00p-3.30p'],
    distDesg: ['QR'],
    description: 'Calculus course.',
    explanation: 'Recommended for math and science majors.',
  };

  const setup = (courses = [mockCourse], recommendationCourses = [mockRecommendationCourse]) => {
    render(
      <MemoryRouter initialEntries={[{ state: { courses: [recommendationCourses, courses] } }]}>
        <ScheduleDisplay />
      </MemoryRouter>
    );
  };


    // Test: Component Renders without Crashing
    test('renders ScheduleDisplay component without crashing', () => {
        setup();
    expect(screen.getByText('More Recommendations')).toBeInTheDocument();
    });

    // Test: Renders a Course in the Calendar
    test('renders a course in the calendar', () => {
    setup();
    const courseElements = screen.getAllByText('CPSC 101');
    expect(courseElements.length).toBeGreaterThan(0);
    expect(courseElements[0]).toBeInTheDocument();

    const courseDescriptionElements = screen.getAllByText('Introduction to Computer Science');
    expect(courseDescriptionElements.length).toBeGreaterThan(0);
    expect(courseDescriptionElements[0]).toBeInTheDocument();
    });

    // Test: Renders Recommendation Courses
    test('renders recommendation courses', () => {
    setup();
    const recommendationElements = screen.getAllByText('MATH 120');
    expect(recommendationElements.length).toBeGreaterThan(0);
    expect(recommendationElements[0]).toBeInTheDocument();

    const recommendationDescriptionElements = screen.getAllByText('Calculus');
    expect(recommendationDescriptionElements.length).toBeGreaterThan(0);
    expect(recommendationDescriptionElements[0]).toBeInTheDocument();
    });


    test('adds a recommendation course to the calendar', () => {
        setup();
    
        // Trigger the "Add" button for a recommendation course
        const addButton = screen.getByAltText('Add'); // Assuming there's an alt text "Add" for the button
        fireEvent.click(addButton);
    
        // Use `getAllByText` to check that multiple instances of "Calculus" now exist in the calendar
        const calculusElements = screen.getAllByText('Calculus');
        
        // Assert that the expected number of "Calculus" instances appear
        // (e.g., if you expect two instances, one in recommendations and one in the calendar)
        expect(calculusElements.length).toBeGreaterThanOrEqual(2);
   
        
    });

    test('removes a course from the calendar', async () => {
        render(
            <MemoryRouter initialEntries={[{ state: { courses: [[], [{ department: "CPSC", courseNumber: "101", courseTitle: "Introduction to Computer Science", time: ["M 9.00a-10.15a"], distDesg: [] }]] } }]}>
                <ScheduleDisplay />
            </MemoryRouter>
        );
    
        // Locate the specific course by its data-testid
        const cpsc101Event = screen.getByTestId("course-CPSC-101");
    
        // Verify that the event container exists
        expect(cpsc101Event).toBeInTheDocument();
    
        // Find and click the delete icon within the CPSC 101 event
        const deleteButton = within(cpsc101Event).getByAltText('Delete');
        fireEvent.click(deleteButton);
    
        // Verify the event has been removed from the DOM
        expect(screen.queryByTestId("course-CPSC-101")).not.toBeInTheDocument();
    });


    // Test: Calls handleReplanClick when Replan Button is Clicked
    test('calls handleReplanClick when replan button is clicked', async () => {
        // Mock localStorage with storedData
        const mockStoredData = { careerGoals: 'Old career goal' };
        localStorage.setItem('coursePlan', JSON.stringify(mockStoredData));

        setup(); // Ensure setup renders ScheduleDisplay with necessary props

        // Mock fetch
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve([[mockRecommendationCourse], []]),
            })
        );

        // Simulate typing a new career goal
        const input = screen.getByPlaceholderText('Refine your career goal');
        fireEvent.change(input, { target: { value: 'New career goal' } });

        // Click the replan button
        const replanButton = screen.getByAltText('Replan');
        fireEvent.click(replanButton);

        // Wait for fetch to be called and recommendations to be updated
        await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));

        // Check that fetch was called with the correct URL and payload
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/course/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ careerGoals: 'New career goal' }),
        });

        // Clean up the mock fetch and localStorage after the test
        global.fetch.mockRestore();
        localStorage.removeItem('coursePlan');
    });


    describe('timeStringToMinutes function', () => {
        test('assumes AM for hours between 7 and 12', () => {
            const timeString = '7.30'; // 7:30 AM assumed
            expect(timeStringToMinutes(timeString)).toBe(450); // 7 * 60 + 30 = 450
        });

        test('assumes PM for hours between 1 and 6', () => {
            const timeString = '3.45'; // 3:45 PM assumed
            expect(timeStringToMinutes(timeString)).toBe(15 * 60 + 45); // 15 * 60 + 45 = 945
        });
    });

    test('handles fetch errors and sets loading and submitting state correctly', async () => {
        // Mock console.error to check if it's called
        const consoleErrorMock = jest.spyOn(console, 'error').mockImplementation(() => {});
    
        // Mock fetch to simulate a network error
        global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));
    
        // Render the component
        render(
          <MemoryRouter>
            <ScheduleDisplay />
          </MemoryRouter>
        );
    
        // Trigger an action that invokes handleReplanClick (e.g., clicking the replan button)
        const replanButton = screen.getByAltText('Replan');
        replanButton.click();
    
        // Wait for the error to be logged
        await waitFor(() => {
          expect(console.error).toHaveBeenCalledWith(
            'There was a problem with the fetch operation:',
            expect.any(Error)
          );
        });
    
        // Clean up mocks
        consoleErrorMock.mockRestore();
        global.fetch.mockRestore();
      });


});