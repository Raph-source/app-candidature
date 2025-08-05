import {Text} from "../../components/form/text.tsx";
import {Input} from "../../components/form/input.tsx";
import {type FieldValues, useForm} from "react-hook-form";
import UseGlobal from "../../hooks/useGlobal.ts";


export const Login = () => {
    const {register, handleSubmit} = useForm()
    const {connexion} = UseGlobal()
    const onSubmit = (data: FieldValues) => {
        connexion(data)
    }
    
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Connectez vous</span> pour profiter</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form onSubmit={handleSubmit((data) => onSubmit(data))}>
                    <div className={"d-round"}>
                        <Input type={"email"} label={"Email"} className={"d-input-login"}
                        register={{...register("email" , {required : true})}}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"password"} label={"Mot de passe"} className={"d-input-login"}
                               register={{...register("mdp" , {required : true})}} />
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
