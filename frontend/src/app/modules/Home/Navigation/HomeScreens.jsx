import React from 'react';
import { Route } from 'react-router-dom';
import Home from '../Screens/Home';


const HomeScreens = (
    <>
        <Route path="/Home" element={<Home />} />
    </>
);

export default HomeScreens;
