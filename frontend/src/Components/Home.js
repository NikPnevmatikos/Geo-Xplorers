import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api';


function Home() {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.REACT_APP_MAPS
  })


  return isLoaded ? (
      <GoogleMap
        mapContainerStyle={{
            width: '100%',
            height: '100vh'
          }}
        center={{
            lat: -3.745,
            lng: -38.523
          }}
        zoom={10}
      >
        <></>
      </GoogleMap>
  ) : <></>
}

export default React.memo(Home)