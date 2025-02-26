import React from 'react';
import { Route } from 'react-router-dom';
import AboutUs from '../Screens/AboutUs';


const AboutUsScreens = (
    <>
        <Route path="/AboutUs" element={<AboutUs />} />
    </>
);

export default AboutUsScreens;
