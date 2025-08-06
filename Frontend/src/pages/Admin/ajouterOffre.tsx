import {Text} from "../../components/form/text.tsx";
import {Input} from "../../components/form/input.tsx";
import {useForm, type FieldValues} from "react-hook-form";

export const AjouterOffre = () => {
    const {register, handleSubmit} = useForm()
    
    const onSubmit = (data : FieldValues) => {
        
    }
    return (
        <div className={"d-container-form"}>
            <Text title={<h3><span>Ajoutez une offre</span> pour profiter</h3>}
                  content={<p>Lorem upsum Lorem upsum Lorem upsum Lorem
                      upsum <span>Lorem upsumLorem upsum</span></p>}/>

            <div className={"d-form"}>
                <form onSubmit={handleSubmit((data : FieldValues) => onSubmit(data))}>
                    <div className={"d-round"}>
                        <Input type={"text"} label={"Titre"} className={"d-input-login"}
                        register={register('email', {required : true})}/>
                    </div>
                    <div className={"d-round"}>
                        <Input type={"textearrea"} label={"Description"} className={"d-input-login"}
                        register={register('description ', {required : true})}/>
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
