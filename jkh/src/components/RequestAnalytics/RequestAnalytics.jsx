import { useEffect, useState } from "react";
import axios from "axios";
import "./styles.css";

const RequestAnalytics = ({ region }) => {

    const [data, setData] = useState(null);
    //const [loading, setLoading] = useState(true);
    //const [error, setError] = useState(null);

    useEffect(() => {
        const getData = async () => {
            try {
                const response = await axios.get(
                    `http://26.115.165.109:8000/visualization/?district=${region}`,
                    { responseType: 'arraybuffer' },
                )
                    .then(response => {
                        const base64 = btoa(
                            new Uint8Array(response.data).reduce(
                                (data, byte) => data + String.fromCharCode(byte),
                                '',
                            ),
                        );
                        return "data:;base64," + base64;
                    });
                setData(response);
                //setError(null);
            } catch (err) {
                //setError(err.message);
                setData(null);
            } finally {
                //setLoading(false);
            }
        };
        getData();
    }, [region]);

    return (
        <div className="RequestAnalytics" >
            <img src={data} alt={'analytics'} />
        </div>
    )
}

export default RequestAnalytics