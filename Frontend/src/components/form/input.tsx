
interface InterfaceINput {
    type : string,
    label : string,
    className? : string
}

export const Input = ( {type,label,className} : InterfaceINput ) => {
    return (
        <div className={"d-input"}>
            <label htmlFor="">{label}</label>
            <input type={type} className={className ?? ""}/>
        </div>
    );
};
