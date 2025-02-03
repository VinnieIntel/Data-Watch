import React from 'react';
import { Route } from 'react-router-dom';
import Error from '../Screens/Error';


const ErrorScreens = (
    <>
        <Route path="/Error" element={<Error />} />
    </>
);

export default ErrorScreens;
