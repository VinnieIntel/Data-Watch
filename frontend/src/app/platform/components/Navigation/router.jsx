import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import UserLayout from '../Layouts/UserLayout';
import Landing from '../../../modules/Landing';
import ErrorScreens from '../../../modules/Error/Navigation/ErrorScreens';
import WikiScreens from '../../../modules/Wiki/Navigation/WikiScreens';
import StatusScreens from '../../../modules/Status/Navigation/StatusScreens';
import HomeScreens from '../../../modules/Home/Navigation/HomeScreens';

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
            </Route>
            
        </>,
    ),
);

export default router;


