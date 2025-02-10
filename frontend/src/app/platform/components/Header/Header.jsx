import styled from 'styled-components';
import { Link /* useNavigate */ } from 'react-router-dom';
import Logo from '../../Icons/logo.png';
import { Button } from '@mui/material';
import PlatformReusableStyles from '../../Style/PlatformReusableStyles';
import COLORS from '../../Style/Colors';

const RootContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 5px solid ${COLORS.lightGreen};
    padding: 30px 60px;
    background-color: var(--component-background-color);
`;

const AuthContainer = styled.div`
    display: flex;
    flex: row;
    gap: 1rem;
`;

export default function Header() {
    // const navigate = useNavigate();

    return (
        <RootContainer>
            <Link to="/">
                <img
                    src={Logo}
                    width={100}
                />
            </Link>
            <AuthContainer>
                <Link to="/">
                    <Button style={{ ...PlatformReusableStyles.SecondaryButtonStyles }}>Log In</Button>
                </Link>
                <Button style={{ ...PlatformReusableStyles.PrimaryButtonStyles }}>Sign Up</Button>
            </AuthContainer>
        </RootContainer>
    );
}