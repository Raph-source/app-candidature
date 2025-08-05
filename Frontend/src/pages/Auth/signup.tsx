import {Input} from "../../components/form/input.tsx";
import {Text} from "../../components/form/text.tsx";
import {type FieldValues, useForm} from "react-hook-form";
import UseGlobal from "../../hooks/useGlobal.ts";

export const Signup = () => {
    const {register, handleSubmit} = useForm()
    const {creerUnCompte} = UseGlobal()
    const onSubmit = (data : FieldValues) => {
        console.log(data)
        creerUnCompte(data)
    }
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Créer un compte</span> et profite</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form  onSubmit={handleSubmit((data) => onSubmit(data))} >
                    <div className={"d-round"}>
                        <Input type={"text"} label={"Nom"} register={{...register('nom', {required : true})}} />
                    </div>
                    <div className={"d-round"}>
                        <Input type={"text"} label={"Post-nom"} register={{...register('post_nom', {required : true})}} />
                        <Input type={"text"} label={"Prenom"} register={{...register('prenom', {required : true})}} />
                    </div>
                    <div className={"d-round"}>
                        <Input type={"email"} label={"Email"} register={{...register('email', {required : true})}} />
                        <Input type={"password"} label={"Mot de passe"} register={{...register('mdp', {required : true})}} />
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
