import React, {useState, useEffect} from 'react'
import {GoogleMap, Marker, MarkerF, useJsApiLoader} from '@react-google-maps/api';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';


function Home() {
    const {isLoaded} = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
    })

    const [mapInstance, setMapInstance] = useState(null);
    const [searchValue, setSearchValue] = useState('');
    const [points, setPoints] = useState([]);

    const handleSearch = () => {
        const keywordPointsMap = {
            Lakes: [
                {lat: 37.77, lng: -122.41},
                {lat: 34.05, lng: -118.24},
                {lat: 57.79, lng: -122.41},
                {lat: 34.05, lng: 118.24},
            ],
            // Add more keyword-point mappings here
        };

        if (searchValue in keywordPointsMap) {
            setPoints(keywordPointsMap[searchValue]);
        } else {
            setPoints([]);
        }
    };

    const handleSearchInputChange = (event) => {
        setSearchValue(event.target.value);
    };

    useEffect(() => {
        if (mapInstance && points.length > 0) {
            const bounds = new window.google.maps.LatLngBounds();
            points.forEach((point) => bounds.extend(point));
            mapInstance.fitBounds(bounds);
        }
    }, [mapInstance, points]);

    return isLoaded ? (
        <div>
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                padding: '10px',
                backgroundColor: '#8ab4f8'
            }}>
                <TextField
                    type="text"
                    value={searchValue}
                    onChange={handleSearchInputChange}
                    label="Search"
                    variant="outlined"
                    style={{marginRight: '10px'}}
                />
                <Button variant="contained" color="primary" onClick={handleSearch}>
                    Search
                </Button>
            </div>
            <GoogleMap
                id="map"
                mapContainerStyle={{
                    width: '100%',
                    height: '100vh'
                }}
                center={points.length > 0 ? points[0] : {lat: 48.8583, lng: 2.2923}}
                zoom={10}
                onLoad={(map) => setMapInstance(map)}
            >
                {points.map((point, index) => (
                    <MarkerF key={index} position={point}/>
                ))}
            </GoogleMap>
        </div>
    ) : <></>
}

export default React.memo(Home)