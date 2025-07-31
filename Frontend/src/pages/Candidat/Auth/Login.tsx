import {Text} from "../../../components/form/text.tsx";
import {Input} from "../../../components/form/input.tsx";


export const Login = () => {
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Connectez vous</span> pour profitera</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form action="">
                    <div className={"d-round"}>
                        <Input type={"email"} label={"Email"} className={"d-input-login"} />
                    </div>
                    <div className={"d-round"}>
                        <Input type={"password"} label={"Mot de passe"} className={"d-input-login"} />
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
