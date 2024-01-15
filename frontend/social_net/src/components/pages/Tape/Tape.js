import Posts from "../../Posts";
import {useEffect, useState} from "react";
import axios from "axios";



const Tape = () => {
    const [appState, setAppState] = useState([]);
    useEffect(() => {
        const apiUrl = 'http://localhost:8000/posts';
        axios.get(apiUrl).then((resp) => {
            const allPersons = resp.data;
            setAppState(allPersons);

        });
    }, [setAppState]);

    return (
        <div className={'tape'}>
            <Posts data={appState.data}></Posts>

        </div>
    )
}


export default Tape