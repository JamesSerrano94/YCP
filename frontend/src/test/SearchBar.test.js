import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from '../Components/SearchBar.js';

describe('SearchBar Component', () => {
  const mockSetCareerGoals = jest.fn();
  const mockHandleReplanClick = jest.fn();

  const setup = (careerGoals = '') => {
    render(
      <SearchBar
        careerGoals={careerGoals}
        setCareerGoals={mockSetCareerGoals}
        handleReplanClick={mockHandleReplanClick}
      />
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders without crashing', () => {
    setup();
    expect(screen.getByPlaceholderText('Refine your career goal')).toBeInTheDocument();
    expect(screen.getByAltText('Choose more')).toBeInTheDocument();
    expect(screen.getByAltText('Replan')).toBeInTheDocument();
  });

  test('displays the correct careerGoals value', () => {
    setup('Software Engineer');
    const input = screen.getByPlaceholderText('Refine your career goal');
    expect(input.value).toBe('Software Engineer');
  });

  test('calls setCareerGoals when typing in the input', () => {
    setup();
    const input = screen.getByPlaceholderText('Refine your career goal');
    fireEvent.change(input, { target: { value: 'Data Scientist' } });
    expect(mockSetCareerGoals).toHaveBeenCalledWith('Data Scientist');
  });

  test('calls handleReplanClick when Enter is pressed', () => {
    setup();
    const input = screen.getByPlaceholderText('Refine your career goal');
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    expect(mockHandleReplanClick).toHaveBeenCalled();
  });

  test('calls handleReplanClick when the search icon is clicked', () => {
    setup();
    const searchIcon = screen.getByAltText('Replan');
    fireEvent.click(searchIcon);
    expect(mockHandleReplanClick).toHaveBeenCalled();
  });
});
