
import {AdminLinks} from "../../components/adminLinks.tsx";
import UseGlobal from "../../hooks/useGlobal.ts";
import {useEffect} from "react";

export const IndexAdmin = () => {


    return (
        <div className={"d-container"}>
            <div className={"d-header"}>
                <h3>Offres<span>App</span></h3>
            </div>
            <div className={"d-content-admin"}>
                <div className={"d-content-head"}>
                    <h3>Espace administrateur</h3>
                    <hr/>
                </div>
                <div className={"d-content-options"}>
                    <AdminLinks label={"Ajouter une offre"} />
                    <AdminLinks label={"Notifier un candidat"} />
                    <AdminLinks label={"Recherchez les candidatures d'un departement"} />
                    <AdminLinks label={"Ajouter une option"} />
                </div>
            </div>
        </div>
    );
};
