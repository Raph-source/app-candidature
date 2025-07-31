import type {ReactElement} from "react";

interface InterfaceText {
    title : ReactElement,
    content : ReactElement
}

export const Text = ({title, content} : InterfaceText) => {
    return (
        <div className={"d-text"}>
            {title}
            {content}
        </div>
    );
};
