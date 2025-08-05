import {Text} from "../../components/form/text.tsx";
import {Input} from "../../components/form/input.tsx";
import {useForm} from "react-hook-form";

export const AjouterOffre = () => {
    const {register, handleSubmit} = useForm()
    c
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Connectez vous</span> pour profiter</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form action="">
                    <div className={"d-round"}>
                        <Input type={"email"} label={"Email"} className={"d-input-login"}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"textearrea"} label={"Description"} className={"d-input-login"}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"date"} label={"Date limite"} className={"d-input-login"}/>
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
