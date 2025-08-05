import {Text} from "../../components/form/text.tsx";
import {Input} from "../../components/form/input.tsx";
import {type FieldValues, useForm} from "react-hook-form";

export const Postuler = () => {
    const {register, handleSubmit} = useForm()
    const onSubmit = (data : FieldValues) => {
        console.log(data)
    }
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Postuler en</span> remplissant le form.</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form onSubmit={handleSubmit((data : FieldValues) =>  onSubmit(data))}>
                    <div className={"d-round"}>
                        <Input type={"file"} label={"Uploder le cv"} className={"d-input-login"}
                        register={register("cv", {required : true})}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"file"} label={"uploder la lettre de motivation"} className={"d-input-login"}
                        register={register("lettre_motivation", {required : true})}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"file"} label={"uploder le diplome"} className={"d-input-login"}
                               register={register("diplome", {required : true})}/>
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        </div>
    );
};
