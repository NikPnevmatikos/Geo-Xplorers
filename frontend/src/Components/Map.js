import React from "react";
import { GoogleMap, useJsApiLoader } from "@react-google-maps/api";

function Map() {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={{
        width: "100%",
        height: "100vh",
      }}
      // center={{
      //   lat: -3.745,
      //   lng: -38.523
      // }}
      center={{
        lat: 37.98381,
        lng: 23.727539,
      }}
      zoom={10}
      options={{
        mapTypeControl: true, // Enable map type control
        mapTypeControlOptions: {
          position: window.google.maps.ControlPosition.BOTTOM_CENTER, // Set position of map type controls
        },
        fullscreenControl: false, // Remove fullscreen button
      }}
    >
      <></>
    </GoogleMap>
  ) : (
    <div>oeoeoeoeoeoeeo the google map is trying to load</div>
  );
}

export default React.memo(Map);
