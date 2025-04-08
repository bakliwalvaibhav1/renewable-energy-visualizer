import {createBrowserRouter, createRoutesFromElements, Route} from "react-router-dom";
// import App from "../App";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import NotFound from "../pages/NotFound";
import AppLayout from "../layout/AppLayout";

export const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path="/" element={<AppLayout />}>
            <Route index element={<Login />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="*" element={<NotFound />} />
        </Route>
    )
);
