import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import  "../public/styles/css/style.css"
import {Signup} from "./pages/Auth/signup.tsx";
import {Login} from "./pages/Auth/Login.tsx";
import {Index} from "./pages/Candidat";
import {IndexAdmin} from "./pages/Admin/indexAdmin.tsx";
import {Details} from "./pages/Candidat/details.tsx";
import {Postuler} from "./pages/Candidat/postuler.tsx";
import {AjouterOffre} from "./pages/Admin/ajouterOffre.tsx";
import {ChearchElement} from "./pages/Admin/chearchElement.tsx";

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
    },
    {
        path : "/details/offre/:idOffre",
        element : <Details/>
    },
    {
        path : "/candidat/postuler/:idoffre/:idepartement",
        element : <Postuler/>
    },
    {
        path : "/admin/",
        children : [
            {
                path : "accueil",
                element : <IndexAdmin/>
            },
            {
                path : "ajouteruneoffrez",
                element : <AjouterOffre/>
            },
            {
                path : "chercher",
                element : <ChearchElement/>
            }
        ]
    }
])

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <RouterProvider router={router} />
    </StrictMode>
)