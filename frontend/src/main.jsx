import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import theme from './app/platform/Theme/theme';
import router from './app/platform/components/Navigation/router';
import GlobalStyle from './app/platform/Style/GlobalStyle';
import './globalStyles/fonts.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
        <GlobalStyle />
            <RouterProvider router={router}></RouterProvider>
    </ThemeProvider>
  </StrictMode>,
)
