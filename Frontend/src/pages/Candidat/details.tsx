import {DetailsOffre} from "../../components/detailsOffre.tsx";
import {CardOffre} from "../../components/cardOffre.tsx";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import UseGlobal from "../../hooks/useGlobal.ts";

export const Details = () => {
    const {idOffre} = useParams()
    const [offre, setOffres] = useState()
    const {getOneOffres} = UseGlobal()

    useEffect(() => {
        getOneOffres(setOffres, idOffre)
    }, []);

    return (
        <div className={"d-container"}>
            <div className={"d-header"}>
                <h3>Offres<span>App</span></h3>
            </div>
            <div className={"d-content-details"}>
                {
                    offre &&   <DetailsOffre offre={offre ?? offre} />
                }

                <div className={"d-middle"}>
                    <h3>Plus d'offres</h3>
                    <hr/>
                </div>
                <div className={"d-others"}>
                    {

                    }

                </div>
            </div>
        </div>
    );
};
