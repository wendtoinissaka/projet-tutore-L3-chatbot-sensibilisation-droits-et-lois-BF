import { useEffect, useState } from 'react';
import axios from 'axios';

function LegalInfoList() {
    const [infoList, setInfoList] = useState([]);

    useEffect(() => {
        async function fetchInfo() {
            try {
                const response = await axios.get('http://localhost:5000/legal-info');
                setInfoList(response.data);
            } catch (error) {
                console.error("There was an error fetching the legal information!", error);
            }
        }
        fetchInfo();
    }, []);

    return (
        <div>
            <h2>Informations Juridiques</h2>
            <ul>
                {infoList.map(info => (
                    <li key={info.id}>{info.title}</li>
                ))}
            </ul>
        </div>
    );
}
export default LegalInfoList;
