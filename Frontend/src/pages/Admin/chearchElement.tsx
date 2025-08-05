
export const ChearchElement = () => {
    return (
        <div className={"d-container"}>
            <div className={"d-header"}>
                <h3>Offres<span>App</span></h3>
            </div>
            <div className={"d-content-admin"}>
                <div className={"d-content-head"}>
                    <div className={"d-content-text"}>
                        <h3>Espace administrateur</h3>
                        <div className={"d-input-chearch"}>
                            <select>
                                <option value="" disabled={true}>Option</option>
                                <option value="">Option</option>
                                <option value="">Option</option>
                            </select>
                            <select>
                                <option value="" disabled={true}>Option</option>
                                <option value="">Option</option>
                                <option value="">Option</option>
                            </select>
                            <button >Envoyer</button>
                        </div>
                    </div>
                    <hr/>
                </div>
                <div className={"d-content-shearch"}>

                </div>
            </div>
        </div>
    );
};
