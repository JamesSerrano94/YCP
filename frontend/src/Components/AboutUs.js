import React from "react";
import { Link } from "react-router-dom";  // Import Link for navigation
import TeamMember from "./TeamMember";  // Create this component for individual team members
import './AboutUs.css';

const AboutUs = () => {
  return (
    <div className="about-us-container">

      <div className="back-arrow-container">
        <Link to="/">
          <button className="back-arrow-button">
            <img src="/back-arrow.svg" alt="Back Arrow" />
          </button>
        </Link>
      </div>

      <div className="header">
        <div>
        <h1>About Us</h1>
        </div>
        <div>
        <p>
          Yale CourseMap offers a personalized course planning tool that considers your major, previous courses, 
          and career aspirations to create your course schedule for an entire semester. This student-led project 
          is from Yale's Software Engineering course.
        </p>
        </div>
      </div>
      
      <div className="team">
        {[...Array(9)].map((_, index) => (
          <TeamMember
            key={index}
            name="Kien Lau"
            role="Frontend Developer"
            intro="I am a front-end developer passionate about building tools to enhance student experiences in course selection."
            imgSrc="/kien_linkedin_headshot.jpg"
          />
        ))}
      </div>
    </div>
  );
};

export default AboutUs;


