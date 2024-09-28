import React from "react";
import TeamMember from "./TeamMember";  // Create this component for individual team members
import './AboutUs.css';
import kienImage from './kien_linkedin_headshot.jpg';

const AboutUs = () => {
  return (
    <div className="about-us-container">
      <div className="header">
        <h1>About Us</h1>
        <p>
          Yale CourseMap offers a personalized course planning tool that considers your major, previous courses, 
          and career aspirations to create your course schedule for an entire semester. This student-led project 
          is from Yale's Software Engineering course.
        </p>
      </div>
      
      <div className="team">
        {[...Array(9)].map((_, index) => (
          <TeamMember
            key={index}
            name="Kien Lau"
            role="Frontend Developer"
            intro="I am a front-end developer passionate about building tools to enhance student experiences in course selection."
            imgSrc={kienImage}
          />
        ))}
      </div>
    </div>
  );
};

export default AboutUs;
