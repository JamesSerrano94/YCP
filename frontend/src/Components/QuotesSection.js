// components/QuotesSection.js
import React from 'react';

const quotes = [
  { text: "I'm interested in animation and visual effects. Can you help me plan my course load to prepare for a career in the film industry?", color: 'rgba(255, 190, 186, 0.64)' },
  { text: "I want to be a Software Development Engineer in the tech industry. Could you help me plan my course schedule for this semester?", color: 'rgba(170, 211, 255, 0.52)' },
  { text: "My goal is to become a quantitative trader. Design a course schedule to build the necessary skills in finance, programming, and quantitative analysis.", color: 'rgba(199, 199, 241, 0.68)' }
];

const QuotesSection = () => (
  <div className="quotes-section">
    {quotes.map((quote, index) => (
      <div key={index} className="quote-card" style={{ backgroundColor: quote.color }}>
        <img src="/frontquote.svg" alt="Front quote" className="quote-icon front-quote" />
        <p>{quote.text}</p>
        <img src="/frontquote.svg" alt="Back quote" className="quote-icon back-quote" />
      </div>
    ))}
  </div>
);

export default QuotesSection;
