import React, { useCallback, useEffect, useState } from "react";
import L from "leaflet";
import "./styles.css";
import useSupercluster from "use-supercluster";
import { Marker, useMap, Popup } from "react-leaflet";

const icons = {};
const fetchIcon = (count, size) => {
    let color;

    if (count < 10) {
        color = "yellow";
    } else if (count < 50) {
        color = "orange";
    } else {
        color = "red";
    }

    if (!icons[count]) {
        icons[count] = L.divIcon({
            html: `
            <div 
                class="cluster-marker ${color}" 
                style="width: ${size * 1.1}px; height: ${size * 1.1}px;">
                ${count}
            </div>`,
        });
    }
    return icons[count];
};

const qmark = new L.Icon({
    iconUrl: "/qmark.png",
    iconSize: [25, 30],
});

const exmark = new L.Icon({
    iconUrl: "/exmark.png",
    iconSize: [25, 30],
});

function Map({ data, center }) {
    const maxZoom = 22;
    const [bounds, setBounds] = useState(null);
    const [zoom, setZoom] = useState(12);
    const map = useMap();

    // get map bounds
    function updateMap() {
        console.log("updating");
        const b = map.getBounds();
        setBounds([
            b.getSouthWest().lng,
            b.getSouthWest().lat,
            b.getNorthEast().lng,
            b.getNorthEast().lat,
        ]);
        setZoom(map.getZoom());
    }

    const onMove = useCallback(() => {
        updateMap();
    }, [map]);

    useEffect(() => {
        if (center) {
            map.setView(center, 18, {
                animate: true,
            });
        }
    }, [center]);

    useEffect(() => {
        updateMap();
    }, [map]);

    useEffect(() => {
        map.on("move", onMove);
        return () => {
            map.off("move", onMove);
        };
    }, [map, onMove]);

    const points = data.map((rqst) => ({
        type: "Feature",
        properties: {
            cluster: false,
            rqstId: rqst.unique_id,
            anomaly: rqst.anomaly,
            description: rqst.description,
            address: rqst.adress_id.adress
        },
        geometry: {
            type: "Point",
            coordinates: [
                rqst.adress_id.longitude,
                rqst.adress_id.latitude,
            ],
        },
    }));

    const { clusters, supercluster } = useSupercluster({
        points: points,
        bounds: bounds,
        zoom: zoom,
        options: { radius: 75, maxZoom: 17 },
    });

    return (
        <>
            {clusters.map((cluster) => {
                // every cluster point has coordinates
                const [longitude, latitude] = cluster.geometry.coordinates;
                // the point may be either a cluster or a point
                const { cluster: isCluster, point_count: pointCount } =
                    cluster.properties;

                // we have a cluster to render
                if (isCluster) {
                    return (
                        <Marker
                            key={`cluster-${cluster.id}`}
                            position={[latitude, longitude]}
                            icon={fetchIcon(
                                pointCount,
                                10 + (pointCount / points.length) * 40
                            )}
                            eventHandlers={{
                                click: () => {
                                    const expansionZoom = Math.min(
                                        supercluster.getClusterExpansionZoom(cluster.id),
                                        maxZoom
                                    );
                                    map.setView([latitude, longitude], expansionZoom, {
                                        animate: true,
                                    });
                                },
                            }}
                        />
                    );
                }

                return (
                    <Marker
                        key={`crime-${cluster.properties.rqstId}`}
                        position={[latitude, longitude]}
                        icon={cluster.properties.anomaly ? exmark : qmark}
                    >
                        <Popup>
                            <div>
                                <h2>{cluster.properties.address}</h2>
                                <p>{cluster.properties.description}</p>
                            </div>
                        </Popup>
                    </Marker>
                );
            })}
        </>
    );
}

export default Map;