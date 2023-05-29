import * as React from "react";
import { GoogleMap, useLoadScript, MarkerF } from "@react-google-maps/api";
import {useMemo} from "react";
import "../Styles/maps.css"


function Home() {
    const { isLoaded } = useLoadScript({
        googleMapsApiKey: "Need to add API key"
    });


    if (!isLoaded) return <div>Loading...</div>;
    return <Map />;
}

function Map() {
    const center = useMemo(() => ({ lat: 48.8583, lng: 2.2923 }), []);
    return <GoogleMap
        zoom={10}
        center={center}
        mapContainerClassName={"map-container"}
    >
        <MarkerF position={center} />
    </GoogleMap>
}

export default Home;