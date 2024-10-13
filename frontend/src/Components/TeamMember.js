import React from "react";

const TeamMember = ({ name, role, intro, imgSrc, linkedin }) => {
  return (
    <div className="team-member-card">
      <img src={imgSrc} alt={name} className="team-member-image" />
      
      <h3 className="team-member-name">
        {name}
        {linkedin && (
          <a href={linkedin} target="_blank" rel="noopener noreferrer">
            <img
              src="/linkedin-icon.svg"
              alt="LinkedIn"
              className="linkedin-icon"
              style={{ marginLeft: '8px', width: '20px', height: '20px' }}
            />
          </a>
        )}
      </h3>

      <p>{role}</p>
      <p className="intro-text">{intro}</p>
    </div>
  );
};

export default TeamMember;

