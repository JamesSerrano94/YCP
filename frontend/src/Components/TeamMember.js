import React from "react";

const TeamMember = ({ name, role, intro, imgSrc }) => {
  return (
    <div className="team-member-card">
      <img src={imgSrc} alt={name} className="team-member-image" />
      <h3>{name}</h3>
      <p>{role}</p>
      <p className="intro-text">{intro}</p>
    </div>
  );
};

export default TeamMember;
