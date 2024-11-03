// teamMember.test.js

import React from 'react';
import { render, screen } from '@testing-library/react';
import TeamMember from  '../Components/TeamMember.js';

describe('TeamMember Component', () => {
  const mockProps = {
    name: 'John Doe',
    role: 'Software Engineer',
    intro: 'Passionate about building scalable web applications.',
    imgSrc: '/path/to/image.jpg',
    linkedin: 'https://linkedin.com/in/johndoe'
  };

  test('renders TeamMember component with all props', () => {
    render(<TeamMember {...mockProps} />);

    // Verify the image source and alt text
    const image = screen.getByAltText('John Doe');
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', mockProps.imgSrc);

    // Verify the name and role text
    expect(screen.getByText(mockProps.name)).toBeInTheDocument();
    expect(screen.getByText(mockProps.role)).toBeInTheDocument();

    // Verify the intro text
    expect(screen.getByText(mockProps.intro)).toBeInTheDocument();

    // Verify LinkedIn link and icon
    const linkedinLink = screen.getByRole('link', { name: /LinkedIn/i });
    expect(linkedinLink).toHaveAttribute('href', mockProps.linkedin);
  });

  test('does not render LinkedIn link if no linkedin prop is provided', () => {
    const { linkedin, ...propsWithoutLinkedIn } = mockProps;
    render(<TeamMember {...propsWithoutLinkedIn} />);

    // Verify LinkedIn icon does not appear when no LinkedIn link is provided
    const linkedinIcon = screen.queryByAltText('LinkedIn');
    expect(linkedinIcon).not.toBeInTheDocument();
  });
});
