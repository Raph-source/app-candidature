import {CardOffre} from "../../components/cardOffre.tsx";
import UseGlobal, {type InterfaceOffres} from "../../hooks/useGlobal.ts";
import {useEffect, useState} from "react";

export const Index = () => {
    const {checkCandidat,getOffre} = UseGlobal()
    const [offres, setOffres] = useState()
    useEffect(() => {
        checkCandidat()
        getOffre(setOffres)

    }, []);
    console.log(offres)

    return (
        <div className={"d-container"}>
            <div className={"d-header"}>
                <h3>Offres<span>App</span></h3>
            </div>
            <div className={"d-content"}>
                {
                    offres && offres.map((offre) => <CardOffre offre={offre}  /> )
                }
            </div>
        </div>
    );
};
