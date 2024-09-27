import React from "react";
import { Card, CardContent, Typography, CardMedia } from "@mui/material";
import styled from "styled-components";

const TeamMember = ({ name, role, intro, imgSrc }) => {
  return (
    <StyledCard>
      <CardMedia component="img" image={imgSrc} alt={name} />
      <CardContent>
        <Typography variant="h5" component="div" gutterBottom>
          {name}
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          {role}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          {intro}
        </Typography>
      </CardContent>
    </StyledCard>
  );
};

// Styled Card using styled-components
const StyledCard = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
  
  &:hover {
    transform: translateY(-10px);
  }

  img {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 0; /* Make the image square */
  }

  .MuiCardContent-root {
    text-align: center;
  }
`;

export default TeamMember;
