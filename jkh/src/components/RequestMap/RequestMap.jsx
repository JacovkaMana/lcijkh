import React from "react";
import "./styles.css";
import Map from "../Map/Map";
import { MapContainer, TileLayer } from "react-leaflet";

const RequestMap = ({ data, region, setRegion, center }) => {

    const regionDict = [
        { name: "Все", value: 0 },
        { name: "ЗАО", value: 800 },
        { name: "СВАО", value: 300 },
        { name: "СЗАО", value: 100 },
        { name: "ЮВАО", value: 500 },
        { name: "САО", value: 900 },
        { name: "ЮЗАО", value: 700 },
        { name: "ЮАО", value: 600 },
        { name: "???", value: 200 },
        { name: "ВАО", value: 400 }
    ]

    return (
        <div className="RequestMap">
            <div className="RequestMap__date">
                <form>
                    <div>
                        Административный округ:
                    </div>
                    <select
                        value={regionDict.find(e => e.value === region).name}
                        onChange={(ev) => setRegion(
                            regionDict.find(e => e.name === ev.target.value).value
                        )}
                    >
                        <option>Все</option>
                        <option>ЗАО</option>
                        {/* <option>ЗелАО/1000</option> */}
                        <option>СВАО</option>
                        <option>СЗАО</option>
                        <option>ЮВАО</option>
                        <option>САО</option>
                        <option>ЮЗАО</option>
                        <option>ЮАО</option>
                        <option>ВАО</option>
                        <option>???</option>
                    </select>
                </form>
            </div>
            <div className="RequestMap__map">
                <MapContainer center={[55.749668, 37.623744]} zoom={11}>
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    />
                    <Map
                        data={data}
                        center={center}
                    />
                </MapContainer>
            </div>
        </div>
    )
}

export default RequestMap