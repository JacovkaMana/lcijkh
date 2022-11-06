import { useEffect, useState } from "react";
import axios from "axios";
import RequestList from "../RequestList/RequestList";
import RequestMap from "../RequestMap/RequestMap";
import RequestAnalytics from "../RequestAnalytics/RequestAnalytics";
import "./styles.css";

const RequestContainer = ({ currentPath }) => {

    const [region, setRegion] = useState(300);
    const [data, setData] = useState(null);
    const [center, setCenter] = useState(null);
    //const [loading, setLoading] = useState(true);
    //const [error, setError] = useState(null);

    useEffect(() => {
        const getData = async () => {
            try {
                const response = await axios.get(
                    `http://26.115.165.109:8000/applications/?district=${region}`
                );
                setData(response.data);
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

    const leftPanel = currentPath === 'analytics'
        ? <RequestAnalytics
            region={region}
        />
        : <RequestList
            data={data}
            center={center}
            setCenter={setCenter}
        />;

    return (
        <div className="RequestContainer">
            {data &&
                <>
                    {leftPanel}
                    <RequestMap
                        data={data}
                        region={region}
                        setRegion={setRegion}
                        center={center}
                    />
                </>}
        </div>
    )
}

export default RequestContainer