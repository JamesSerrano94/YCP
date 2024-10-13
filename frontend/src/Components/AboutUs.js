import React from "react";
import { Link } from "react-router-dom";  // Import Link for navigation
import TeamMember from "./TeamMember";  // Component for individual team members
import './AboutUs.css';

const AboutUs = () => {
  const teamMembers = [
    {
      name: "Bella Bao",
      role: "Product Manager & Frontend Engineer",
      intro: "Bring together product design and development to create cool product!",
      imgSrc: "/BellaPhoto.jpeg",
      linkedin: "https://www.linkedin.com/in/bella-bao-521265202/",
    },
    {
      name: "Kien Lau",
      role: "Frontend Engineer",
      intro: "I am a front-end developer passionate about building tools to enhance student experiences in course selection.",
      imgSrc: "/kien_linkedin_headshot.jpg",
    },
    {
      name: "Xiatao Sun",
      role: "Backend Engineer",
      intro: "I work on backend systems to ensure fast and reliable data services for course recommendations.",
      imgSrc: "/bulldog.jpg",
    },
    {
      name: "Yangtian Zhang",
      role: "Backend Engineer",
      intro: "I work on backend systems to ensure fast and reliable data services for course recommendations.",
      imgSrc: "/bulldog.jpg",
    },
    {
      name: "James Serrano",
      role: "Backend Engineer",
      intro: "I work on backend systems to ensure fast and reliable data services for course recommendations.",
      imgSrc: "/bulldog.jpg",
    },
    {
      name: "Yang Zhou",
      role: "Backend Developer",
      intro: "I work on backend systems to ensure fast and reliable data services for course recommendations.",
      imgSrc: "/bulldog.jpg",
    },
  ];

  return (
    <div className="about-us-container">
      {/* Back arrow for navigation */}
      <div className="back-arrow-container">
        <Link to="/">
          <button className="back-arrow-button">
            <img src="/back-arrow.svg" alt="Back Arrow" />
          </button>
        </Link>
      </div>

      {/* Header with description */}
      <div className="header">
        <h1>About Us</h1>
        <p>
          Yale CourseMap offers a personalized course planning tool that considers your major, previous courses, 
          and career aspirations to create your course schedule for an entire semester. This student-led project 
          is from Yale's Software Engineering course.
        </p>
      </div>

      {/* Team section */}
      <div className="team">
        {teamMembers.map((member, index) => (
          <TeamMember
            key={index}
            name={member.name}
            role={member.role}
            intro={member.intro}
            imgSrc={member.imgSrc}
            linkedin={member.linkedin}
          />
        ))}
      </div>
    </div>
  );
};

export default AboutUs;



