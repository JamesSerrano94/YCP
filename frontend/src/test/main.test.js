// main.test.js

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MainPage from '../Components/main';
import { MemoryRouter } from 'react-router-dom';

// Mock scrollIntoView since it's not implemented in jsdom
beforeAll(() => {
  Element.prototype.scrollIntoView = jest.fn();
});

describe('MainPage Component', () => {
  test('renders without crashing', () => {
    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    const appNameElement = screen.getByTestId('app-name');
    expect(appNameElement).toBeInTheDocument();
  });

  test('clicking "Start planning!" button calls scrollIntoView', () => {
    const scrollIntoViewMock = jest.fn();
    Element.prototype.scrollIntoView = scrollIntoViewMock;

    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    const startButton = screen.getByText(/Start planning!/i);
    fireEvent.click(startButton);
    expect(scrollIntoViewMock).toHaveBeenCalled();
  });

  test('shows alert when career goals are empty and Plan button is clicked', () => {
    window.alert = jest.fn();

    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    const planButton = screen.getByText(/^Plan$/i);
    fireEvent.click(planButton);
    expect(window.alert).toHaveBeenCalledWith('Please fill out your career goals.');
  });

//   test('sends POST request with correct data when Plan button is clicked', async () => {
//     const mockFetch = jest.fn(() =>
//       Promise.resolve({
//         ok: true,
//         json: () => Promise.resolve({ message: 'Success' }),
//       })
//     );
//     global.fetch = mockFetch;
//     process.env.REACT_APP_API_URL = 'http://localhost:8000';
  
//     render(
//       <MemoryRouter>
//         <MainPage />
//       </MemoryRouter>
//     );
  
//     // Fill out required fields
//     fireEvent.change(screen.getByPlaceholderText(/e\.g\. I want to be a game developer\.\.\./i), {
//       target: { value: 'I want to be a game developer.' },
//     });
//     fireEvent.change(screen.getByPlaceholderText(/e\.g\. MATH 225, CPSC 201, CPSC 223, CPSC 323/i), {
//       target: { value: 'MATH 225, CPSC 201' },
//     });
  
//     const planButton = screen.getByText(/^Plan$/i);
//     fireEvent.click(planButton);
  
//     await waitFor(() => expect(mockFetch).toHaveBeenCalled());
  
//     const expectedData = {
//       major: 'Computer Science',
//       semester: 'Spring 2025',
//       schedulePreferences: {
//         earliestStartTime: '8:00 AM',
//         latestEndTime: '9:00 PM',
//       },
//       careerGoals: 'I want to be a game developer.',
//       fulfilledRequirements: {
//         priorCourses: ['MATH 225', 'CPSC 201'],
//       },
//       needDistributionals: {
//         humanities: 0,
//         sciences: 0,
//         social: 0,
//         qr: 0,
//         writing: 0,
//         language: '',
//       },
//     };
//     const apiUrl = process.env.REACT_APP_API_URL;
//     expect(mockFetch).toHaveBeenCalledWith(
//       `${apiUrl}/course/recommend`,
//       {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(expectedData),
//       }
//     );
//   });

  describe('MainPage Component - Form Elements', () => {

    test('updates semester select correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const semesterSelect = screen.getByLabelText('Semester');
      expect(semesterSelect.value).toBe('Spring 2025'); // Default value
  
      // Change semester to "Spring 2025"
      fireEvent.change(semesterSelect, { target: { value: 'Spring 2025' } });
      expect(semesterSelect.value).toBe('Spring 2025');
    });
  
    test('updates earliest start time select correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const earliestStartTimeSelect = screen.getByLabelText('Earliest Start Time');
      expect(earliestStartTimeSelect.value).toBe('8:00 AM');
  
      // Change earliest start time to "10:00 AM"
      fireEvent.change(earliestStartTimeSelect, { target: { value: '10:00 AM' } });
      expect(earliestStartTimeSelect.value).toBe('10:00 AM');
    });
  
    test('updates latest end time select correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const latestEndTimeSelect = screen.getByLabelText('Latest End Time');
      expect(latestEndTimeSelect.value).toBe('5:00 PM'); // Assuming default is '5:00 PM'
  
      // Change latest end time to "6:00 PM"
      fireEvent.change(latestEndTimeSelect, { target: { value: '6:00 PM' } });
      expect(latestEndTimeSelect.value).toBe('6:00 PM');
    });
  
    test('updates humanities input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const humanitiesInput = screen.getByLabelText('Humanities');
      expect(humanitiesInput.value).toBe('0'); // Assuming default is 0
  
      // Change humanities value to 1
      fireEvent.change(humanitiesInput, { target: { value: '1' } });
      expect(humanitiesInput.value).toBe('1');
    });
  
    test('updates sciences input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const sciencesInput = screen.getByLabelText('Sciences');
      expect(sciencesInput.value).toBe('0'); // Assuming default is 0
  
      // Change sciences value to 1
      fireEvent.change(sciencesInput, { target: { value: '1' } });
      expect(sciencesInput.value).toBe('1');
    });
  
    test('updates social input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const socialInput = screen.getByLabelText('Social');
      expect(socialInput.value).toBe('0'); // Assuming default is 0
  
      // Change social value to 1
      fireEvent.change(socialInput, { target: { value: '1' } });
      expect(socialInput.value).toBe('1');
    });
  
    test('updates qr input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const qrInput = screen.getByLabelText('QR');
      expect(qrInput.value).toBe('0'); // Assuming default is 0
  
      // Change qr value to 1
      fireEvent.change(qrInput, { target: { value: '1' } });
      expect(qrInput.value).toBe('1');
    });
  
    test('updates writing input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const writingInput = screen.getByLabelText('Writing');
      expect(writingInput.value).toBe('0'); // Assuming default is 0
  
      // Change writing value to 1
      fireEvent.change(writingInput, { target: { value: '1' } });
      expect(writingInput.value).toBe('1');
    });
  
    test('updates language input correctly', () => {
      render(
        <MemoryRouter>
          <MainPage />
        </MemoryRouter>
      );
  
      const languageInput = screen.getByLabelText('Language');
      expect(languageInput.value).toBe(''); // Assuming default is an empty string
  
      // Change language value to "L3 SPAN"
      fireEvent.change(languageInput, { target: { value: 'L3 SPAN' } });
      expect(languageInput.value).toBe('L3 SPAN');
    });
  
  });
  
  test('handles fetch error when network response is not ok', async () => {
    const consoleErrorMock = jest.spyOn(console, 'error').mockImplementation(() => {});
    global.fetch = jest.fn(() => Promise.resolve({ ok: false }));

    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByPlaceholderText(/e\.g\. I want to be a game developer\.\.\./i), {
      target: { value: 'I want to be a game developer.' },
    });

    const planButton = screen.getByText(/^Plan$/i);
    fireEvent.click(planButton);

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
    expect(consoleErrorMock).toHaveBeenCalledWith(
      'There was a problem with the fetch operation:',
      expect.any(Error)
    );

    consoleErrorMock.mockRestore();
  });

  test('logs response data when fetch succeeds', async () => {
    const consoleLogMock = jest.spyOn(console, 'log').mockImplementation(() => {});
    const mockResponseData = { message: 'Success' };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponseData),
      })
    );

    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByPlaceholderText(/e\.g\. I want to be a game developer\.\.\./i), {
      target: { value: 'I want to be a game developer.' },
    });

    const planButton = screen.getByText(/^Plan$/i);
    fireEvent.click(planButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();  
    });

    consoleLogMock.mockRestore();
  });

  test('updates major select correctly', () => {
    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );
    const majorSelect = screen.getByLabelText(/Major/i);
    expect(majorSelect.value).toBe('Computer Science');

    fireEvent.change(majorSelect, { target: { value: 'Mathematics' } });
    expect(majorSelect.value).toBe('Mathematics');
  });
});
