import React from "react";
import TeamMember from "./TeamMember";
import { Container, Typography, Grid } from "@mui/material"; // Import Material UI components
import styled from "styled-components"; // Import styled-components for custom styles
import kienImage from './kien_linkedin_headshot.jpg';

const AboutUs = () => {
  return (
    <CustomContainer>
      <HeaderContainer>
        <Typography variant="h2" gutterBottom>
          About Us
        </Typography>
        <Typography variant="body1" align="center">
          Yale CourseMap offers a personalized course planning tool that considers your major, previous courses, 
          and career aspirations to create your course schedule for an entire semester. This student-led project 
          is from Yale's Software Engineering course.
        </Typography>
      </HeaderContainer>

      <GridContainer container spacing={4}>
        {[...Array(9)].map((_, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <TeamMember
              name="Kien Lau"
              role="Frontend Developer"
              intro="I am a front-end developer passionate about building tools to enhance student experiences in course selection."
              imgSrc={kienImage}
            />
          </Grid>
        ))}
      </GridContainer>
    </CustomContainer>
  );
};

// Styled-components for custom styling
const CustomContainer = styled(Container)`
  background-color: #f5f8ff;
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const HeaderContainer = styled.div`
  text-align: center;
  margin-bottom: 40px;
`;

const GridContainer = styled(Grid)`
  max-width: 1200px;
  width: 100%;
  justify-content: center;
`;

export default AboutUs;
