import {Input} from "../../../components/form/input.tsx";
import {Text} from "../../../components/form/text.tsx";

export const Signup = () => {
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Créer un compte</span> et profite</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form action="">
                    <div className={"d-round"}>
                        <Input type={"text"} label={"Nom"} />
                    </div>
                    <div className={"d-round"}>
                        <Input type={"text"} label={"Post-nom"} />
                        <Input type={"text"} label={"Prenom"} />
                    </div>
                    <div className={"d-round"}>
                        <Input type={"email"} label={"Email"} />
                        <Input type={"password"} label={"Mot de passe"} />
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
