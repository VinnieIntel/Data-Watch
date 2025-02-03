import React from 'react';
import { Route } from 'react-router-dom';
import Status from '../Screens/Status';

const StatusScreens = (
    <>
        <Route path="/Status" element={<Status />} />
    </>
);

export default StatusScreens;
