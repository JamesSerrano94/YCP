import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import AboutUs from '../Components/AboutUs.js';

describe('AboutUs Component', () => {
  test('renders About Us page header and description', () => {
    render(
      <MemoryRouter>
        <AboutUs />
      </MemoryRouter>
    );

    // Verify the header and description text
    expect(screen.getByRole('heading', { name: /About Us/i })).toBeInTheDocument();
    expect(screen.getByText(/Yale CourseMap offers a personalized course planning tool/i)).toBeInTheDocument();
  });

  test('renders all team members with correct information', () => {
    render(
      <MemoryRouter>
        <AboutUs />
      </MemoryRouter>
    );

    // Check each team member’s name and role
    const teamMembers = [
      { name: 'Bella Bao', role: 'Product Manager & Frontend Engineer' },
      { name: 'Kien Lau', role: 'Frontend Engineer' },
      { name: 'Xiatao Sun', role: 'Backend Engineer' },
      { name: 'Yangtian Zhang', role: 'Backend Engineer' },
      { name: 'James Serrano', role: 'Backend Engineer' },
      { name: 'Yang Zhou', role: 'Backend Developer' }
    ];

    teamMembers.forEach((member) => {
      expect(screen.getByText(member.name)).toBeInTheDocument();
    });

    // Verify roles using getAllByText for repeated roles
    expect(screen.getAllByText('Backend Engineer').length).toBe(3);
    expect(screen.getByText('Frontend Engineer')).toBeInTheDocument();
    expect(screen.getByText('Product Manager & Frontend Engineer')).toBeInTheDocument();
    expect(screen.getByText('Backend Developer')).toBeInTheDocument();
  });

  test('renders LinkedIn icon with link for members with linkedin prop', () => {
    render(
      <MemoryRouter>
        <AboutUs />
      </MemoryRouter>
    );

    // Verify Bella Bao's LinkedIn link
    const linkedinLink = screen.getByRole('link', { name: /LinkedIn/i });
    expect(linkedinLink).toHaveAttribute('href', 'https://www.linkedin.com/in/bella-bao-521265202/');
  });

  test('renders back arrow with link to home page', () => {
    render(
      <MemoryRouter>
        <AboutUs />
      </MemoryRouter>
    );

    // Check back arrow navigation button
    const backButton = screen.getByRole('button', { name: /Back Arrow/i });
    expect(backButton).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Back Arrow/i })).toHaveAttribute('href', '/');
  });
});
