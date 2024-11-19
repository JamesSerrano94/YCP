import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TooltipIcon from '../Components/TooltipIcon.js';
import '@testing-library/jest-dom';

describe('TooltipIcon Component', () => {
  test('renders the tooltip icon without crashing', () => {
    render(<TooltipIcon title="This is a tooltip message" />);
    const icon = screen.getByAltText('Info icon');
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveAttribute('src', '/alert-circle.svg');
    expect(icon).toHaveStyle({ width: '20px', height: '20px', cursor: 'pointer' });
  });

});
