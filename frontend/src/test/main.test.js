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

  test('sends POST request with correct data when Plan button is clicked', async () => {
    const mockFetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: 'Success' }),
      })
    );
    global.fetch = mockFetch;

    render(
      <MemoryRouter>
        <MainPage />
      </MemoryRouter>
    );

    // Fill out required fields
    fireEvent.change(screen.getByPlaceholderText(/e\.g\. I want to be a game developer\.\.\./i), {
      target: { value: 'I want to be a game developer.' },
    });
    fireEvent.change(screen.getByPlaceholderText(/e\.g\. MATH 225, CPSC 201, CPSC 323/i), {
      target: { value: 'MATH 225, CPSC 201' },
    });

    const planButton = screen.getByText(/^Plan$/i);
    fireEvent.click(planButton);

    await waitFor(() => expect(mockFetch).toHaveBeenCalled());

    const expectedData = {
      major: 'Computer Science',
      semester: 'Fall 2024',
      schedulePreferences: {
        earliestStartTime: '8:00 AM',
        latestEndTime: '9:00 PM',
      },
      careerGoals: 'I want to be a game developer.',
      fulfilledRequirements: {
        humanities: [],
        sciences: [],
        social: [],
        qr: [],
        writing: [],
        language: [],
        priorCourses: ['MATH 225', 'CPSC 201'],
      },
    };

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/course/recommend',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(expectedData),
      }
    );
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
      expect(consoleLogMock).toHaveBeenCalledWith(mockResponseData);
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
