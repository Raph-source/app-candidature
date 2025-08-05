import {Link} from "react-router-dom";

interface InterfaceOffreDetails {
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
export const DetailsOffre = ({offre}  : InterfaceOffreDetails) => {


    return (
        <div className={"d-details"}>
            <div className={"d-details-container"}>
                <div className={"d-color"}>
                    <Link to={"/candidat/accueil"} className={"d-back"}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="32"
                            height="32"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="#000000"
                            stroke-width="1"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <path d="M15 6l-6 6l6 6" />
                        </svg>

                    </Link>
                </div>
                <div className={"d-details-text"}>
                    <h3>{offre.titre}r</h3>
                    <p>{offre.description}</p>
                    <div className={"d-badges"}>
                        <span>{offre.departement.nom}</span><span>{offre.date_limite}</span>
                    </div>
                    <Link to={`/candidat/postuler/${offre.id}`}>Postuler</Link>
                </div>
            </div>
        </div>
    );
};
