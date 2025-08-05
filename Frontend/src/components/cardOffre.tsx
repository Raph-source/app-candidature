import {Link} from "react-router-dom";

interface InterfaceCardOffre {
    offre : {
        date_limite: string,
        titre: string,
        description: string,
        id : string,
        id_departement: number,
        departement: {
            nom: string,
            id: string
        }
    }
}

export const CardOffre = ( {offre} : InterfaceCardOffre ) => {
    const bgcolor = [
        {
            color : "#c5f1ff"
        },
        {
            color : "#ffc5c5"
        },
        {
            color : "#ffc5c5"
        },
        {
            color : "#b2ffe8"
        },
        {
            color : "#bcb2ff"
        },
        {
            color : "#fffbb2"
        }
    ]
    const colorRadmon  = bgcolor[Math.floor(Math.random() * bgcolor.length)];
    return (
        <Link className={"d-card-offre"} to={`/details/offre/${offre.id}`}>
            <div className={"d-color"} style={{backgroundColor : colorRadmon.color}}>

            </div>
            <div className={"d-bottom"}>
                <h3>{offre.titre}</h3>
                <div className={"d-span"}>
                    <span className={"d-round-color"}></span>
                    <span>{offre.date_limite}</span>
                </div>
            </div>
        </Link>
    );
};
