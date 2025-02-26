import { NavLink } from 'react-router-dom';
import styled from 'styled-components';
import COLORS from '../../Style/Colors';
import FONTSIZE from '../../Style/FontSize';
import NavLinkUtils from '../../Utils/NavLinkUtils';

const NavList = styled.ul`
  list-style: none;
  padding: 0;
  border-right: 5px solid ${COLORS.lightGreen};  
  flex-grow: 1; 
`;

const NavLinkContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-right: 1rem;
    margin-top:30px;
    background-color: var(--component-background-color);
`;

const AboutSection = styled.div`
 display: flex;
 flex-direction: column;
  border-top: 1px solid #4a5568; /* Border to separate */
  margin-top: auto; /* Pushes this section to the bottom */
`;

const StyledNavLink = styled(NavLink)`
    text-decoration: none;
    font-size: ${FONTSIZE.medium};
    padding: 0.5rem 1rem;
    transition: background-color 0.3s;
    border-radius: 10px;

    /* region animation */
    &:after {
        transition: all ease-in-out 0.3s;
        content: '';
        display: block;
        height: 2px;
        width: 0;
    }

    &:hover {
        background-color: ${COLORS.lightestGreen};
    }

    &:hover:after {
        width: 100%;
    }
`;

export default function SideNav() {
    return (
        <NavList>
            <NavLinkContainer>
                <StyledNavLink
                    to="/Home"
                    style={NavLinkUtils.activeStyleWithFontWeight}
                >
                    Home
                </StyledNavLink>
                <StyledNavLink
                    to="/Wiki"
                    style={NavLinkUtils.activeStyleWithFontWeight}
                >
                    Wiki
                </StyledNavLink>
                <StyledNavLink
                    to="/Status"
                    style={NavLinkUtils.activeStyleWithFontWeight}
                >
                    Status
                </StyledNavLink>
                <StyledNavLink
                    to="/Error"
                    style={NavLinkUtils.activeStyleWithFontWeight}
                >
                    Error
                </StyledNavLink>
                </NavLinkContainer>
                
                <NavLinkContainer>
                <AboutSection>
                <StyledNavLink
                    to="/AboutUs"
                    style={NavLinkUtils.activeStyleWithFontWeight}
                >
                    About Us
                </StyledNavLink>
                
                </AboutSection>
                </NavLinkContainer>
            
        </NavList>
    );
}