// components/TooltipIcon.js
import React from 'react';
import { Tooltip } from '@mui/material';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

const HtmlTooltip = styled(({ className, ...props }) => (
  <Tooltip {...props} classes={{ popper: className }} arrow>
    {props.children}
  </Tooltip>
))(({ theme }) => ({
  [`& .MuiTooltip-tooltip`]: {
    backgroundColor: '#ffffff',
    color: '#333333',
    maxWidth: 500,
    border: '1px solid #dadde9',
    boxShadow: '0px 2px 10px rgba(0, 0, 0, 0.2)',
    padding: '10px',
  },
  [`& .MuiTooltip-arrow`]: {
    color: '#ffffff',
  },
}));

const TooltipIcon = ({ title }) => (
  <HtmlTooltip
    title={
      <Typography color="inherit" variant="body2">
        {title}
      </Typography>
    }
  >
    <img src="/alert-circle.svg" alt="Info icon" style={{ width: 20, height: 20, cursor: 'pointer' }} />
  </HtmlTooltip>
);

export default TooltipIcon;
