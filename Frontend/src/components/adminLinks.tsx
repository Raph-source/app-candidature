import {Link} from "react-router-dom";


interface LinksType {
    label : string
}
export const AdminLinks = ({ label} : LinksType) => {
    return (
        <Link to={"#"}>
            <span>{label}</span>
        </Link>
    );
};
