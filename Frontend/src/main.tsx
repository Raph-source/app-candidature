import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import  "../public/styles/css/style.css"
import {Signup} from "./pages/Candidat/Auth/signup.tsx";
import {Login} from "./pages/Candidat/Auth/Login.tsx";
import {Index} from "./pages/Candidat";

const router = createBrowserRouter([
    {
        path : "/",
        element : <Login/>
    },
    {
        path : "/connexion",
        element : <Login/>
    },
    {
        path : "/creer/un/compte",
        element : <Signup/>
    },
    {
        path : "/candidat/accueil",
        element : <Index/>
    }
])

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <RouterProvider router={router} />
    </StrictMode>
)