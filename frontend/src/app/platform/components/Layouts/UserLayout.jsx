import styled from 'styled-components';
import Header from '../Header/Header';
import SideNav from '../SideNav/SideNav';
import { Outlet } from 'react-router-dom';
import * as React from 'react';
import { useRef, useState, useEffect } from 'react';

const LayoutContainer = styled.div`
    display: flex;
    flex-direction: column;
    height: 100vh;
`;

const HeaderContainer = styled.div`
    position: fixed;
    width: 100%;
    left: 50%; 
    transform: translateX(-50%);
    z-index: 2;
`;

const SideNavContainer = styled.div`
    position: fixed;
    flex-shrink: 0;
    left: 40px;
    width: 160px;
    overflow-y: auto;
    z-index: 2;
`;

const ContentContainer = styled.div`
    display: flex;
    margin-top: 170px;
    height: calc(100vh - 60px);
`;

const MainContent = styled.div`
    margin-left: 200px;
    width: calc(100% - 200px);
    padding: 2rem;
`;


export default function UserLayout() {
    return (
        <LayoutContainer>
            <HeaderContainer>
                <Header />
            </HeaderContainer>
            <ContentContainer>
                <SideNavContainer>
                    <SideNav />
                </SideNavContainer>
                <MainContent>
                    <Outlet />
                </MainContent>
            </ContentContainer>
        </LayoutContainer>
    );
}

