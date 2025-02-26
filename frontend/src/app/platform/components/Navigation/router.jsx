import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import UserLayout from '../Layouts/UserLayout';
import Landing from '../../../modules/Landing';
import ErrorScreens from '../../../modules/Error/Navigation/ErrorScreens';
import WikiScreens from '../../../modules/Wiki/Navigation/WikiScreens';
import StatusScreens from '../../../modules/Status/Navigation/StatusScreens';
import HomeScreens from '../../../modules/Home/Navigation/HomeScreens';
import AboutUsScreens from '../../../modules/AboutUs/Navigation/AboutUsScreens';

const router = createBrowserRouter(
    createRoutesFromElements(
        <>
            <Route
                path="/"
                element={<Landing />}
            />
            <Route element={<UserLayout />}>
                {HomeScreens}
                {WikiScreens}
                {StatusScreens}
                {ErrorScreens}
                {AboutUsScreens}
            </Route>
            
        </>,
    ),
);

export default router;


