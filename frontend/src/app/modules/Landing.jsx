import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import PlatformReusableStyles from '../platform/Style/PlatformReusableStyles';
import { Button } from '@mui/material';
import Logo from '.././platform/Icons/logo.png';

const StyledDiv = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;

`;
const ButtonsDiv = styled.div`
    display: flex;
    gap: 2rem;
    padding: 1rem;
    justify-content: center;
`;

const Landing = () => {
    return (
        <div>
            <StyledDiv>
                <img
                    src={Logo}
                    width={300}
                />
                <h1>Welcome to Data Watch</h1>
            
            <ButtonsDiv>
                <Link to="/Home">
                    <Button style={PlatformReusableStyles.PrimaryButtonStyles}>Login</Button>
                </Link>
            </ButtonsDiv>
            </StyledDiv>
        </div>
    );
};
console.log("API URL:", import.meta.env.VITE_API_URL);

export default Landing;
