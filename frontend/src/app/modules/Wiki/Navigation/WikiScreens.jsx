import React from 'react';
import { Route } from 'react-router-dom';
import Wiki from '../Screens//Wiki';
import WikiRule from '../Screens/WikiRule';


const WikiScreens = (
    <>
        <Route path="/Wiki" element={<Wiki />} />
        <Route path="/Wiki/:ruleId" element={<WikiRule />} /> {/* Dynamic parameter */}
    </>
);

export default WikiScreens;
