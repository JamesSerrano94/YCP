// CourseDetailsTooltip.js
import React from 'react';
import { styled } from '@mui/material/styles';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';


const HtmlTooltip = styled(({ className, ...props }) => (
  <Tooltip {...props} classes={{ popper: className }} arrow>
    {props.children}
  </Tooltip>
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    backgroundColor: '#ffffff',
    color: '#333333',
    maxWidth: 500,
    border: '1px solid #dadde9',
    boxShadow: '0px 2px 10px rgba(0, 0, 0, 0.2)',
    padding: '10px',
  },
  [`& .${tooltipClasses.arrow}`]: {
    color: '#ffffff',
  },
}));

const CourseDetailsTooltip = ({ course, children }) => {
  return (
    <HtmlTooltip
      title={
        <React.Fragment>
          <Typography color="inherit" variant="h6">
            {course.courseTitle}
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>Course time:</strong> {course.time}
          </Typography>
          {course.distDesg && course.distDesg.length > 0 && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              <strong>Fulfilled Distributional:</strong> {course.distDesg.join(', ')}
            </Typography>
          )}
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>Course description:</strong> {course.description}
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>Why do we recommend it:</strong> {course.explanation}
          </Typography>
        </React.Fragment>
      }
    >
      {children}
    </HtmlTooltip>
  );
};

export default CourseDetailsTooltip;
