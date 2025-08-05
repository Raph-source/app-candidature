
interface InterfaceINput {
    type : string,
    label : string,
    className? : string,
    register : object
}

export const Input = ( {type,label,className ,register} : InterfaceINput ) => {
    return (
        <div className={"d-input"}>
            <label htmlFor="">{label}</label>
            {type === "textearrea" ? <textarea name="" id="" ></textarea> :
                <input type={type} className={className ?? ""} {...register}/>
            }

        </div>
    );
};
