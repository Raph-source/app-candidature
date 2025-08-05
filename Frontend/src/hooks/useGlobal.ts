import {useNavigate} from "react-router-dom";
import axios from "axios";
import type {FieldValues} from "react-hook-form";

export interface InterfaceOffres {
    offre : {
        id: number,
        date_limite: string,
        titre: string,
        description: string,
        id_departement: number,
        departement: {
            nom: string,
            id: string
        }
    }[]
}
const UseGlobal =  () => {
    const racine = "http://127.0.0.1:8000/"
    const navigate = useNavigate()

    const checkCandidat = async () =>{
        const user = localStorage.getItem('candidat')
        if (!(user)){
            navigate("/")
        }
    }
    const checkAdmin = async () =>{
        const user = localStorage.getItem('admin')
        if (!(user)){
            navigate("/")
        }
    }

    const axiosSend = async (action : string, url : string, data? : FieldValues) => {
        const urlComplet =  racine+url
        try {
            const response = action == "post" ? await axios.post(`${urlComplet}`, data, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            }) : await axios.get(urlComplet)
            return  response
        }
        catch (e) {
            alert('Erreur')
            console.log(e)
            return  e
        }
    }
    const connexion = async ( data : FieldValues) =>{
        const url = "candidat/login"
        console.log(data)
        try {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            const response = await axiosSend("post", url,data)
            console.log(response)
            localStorage.setItem("candidat" ,response.data.message.id)
            navigate("/candidat/accueil")
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        }catch (e) {
            alert("Erreur : Vous n'avez pas un compte")
        }
    }
    const postuler = async (data : FieldValues) =>{
        const url = "candidat/postuler"
        const urlComplet =  racine+url
        try {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            await axiosSend("post", url,data)
            await axios.post(`${urlComplet}`, data, {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    }
            })
            alert('Vous avez postuler !!')
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
        }catch (e) {
            alert("Erreur : Vous n'avez pas un compte")
        }
    }
    const creerUnCompte = async ( data : FieldValues) =>{
        const url = "candidat/signup"

        try {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            await axiosSend("post",url,data)
            alert("Compte crée avec un succées")
            navigate('/')
        }
        catch (e) {
            console.log(e)
            alert("Erreur : Vous n'avez pas un compte")
        }

    }
    const getOffre = async  (setOffre : () => void) => {
        const url = "candidat/offres"
        try {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            const response : { data :  InterfaceOffres  }  = await axiosSend("get",url)
            setOffre(response.data)
            //seetOffres(response.ata)
            console.log(response.data)
        }
        catch (e) {
            console.log(e)
            alert("Erreur : Vous n'avez pas un compte")
        }
    }
    const getOneOffres = async  (setOneOffre : () => void, idOffres : string) => {
        const url = "candidat/offres"
        try {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            const response : { data :  InterfaceOffres  }  = await axiosSend("get",url)
            console.log(response.data)
            const oneOffres = response.data.filter((offr) => offr.id === Number(idOffres) )
            console.log(oneOffres[0])

            setOneOffre(oneOffres[0])
            //seetOffres(response.ata)
        }
        catch (e) {
            console.log(e)
            alert("Erreur : Vous n'avez pas un compte")
        }
    }

    return {connexion, creerUnCompte,getOffre,postuler,
        checkAdmin, checkCandidat, getOneOffres}
}

export default UseGlobal