import React, {useState, useEffect, useRef} from 'react'
import {GoogleMap, Marker, MarkerF, useJsApiLoader} from '@react-google-maps/api';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import html2canvas from 'html2canvas';


function Home() {
    const {isLoaded} = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
        
    })
    const [mapInstance, setMapInstance] = useState(null);
    const [searchValue, setSearchValue] = useState('');
    const [points, setPoints] = useState([]);
    const mapRef = useRef(null);
    let dataUrl = null;

    const [categories, setCategories] = useState([]);

    const handleCategoriesClick = async () => {
      const response = await fetch("http://localhost:8000/api/search/categories");
      const data = await response.json();
      setCategories(data);
    };
  
    const handleCategoryChange = (event) => {
      const categoryName = event.target.value;
      const isChecked = event.target.checked;
      if (isChecked) {
        setCategories([...categories, categoryName]);
      } else {
        setCategories(categories.filter((category) => category !== categoryName));
      }
    };

    const handleSearch = async () => {
        const requestBody = {
            filters: {
                categories: [],
                keywords: [],
                distance: {},
            },
            text: "test",
        };

        try {
            console.log("searching");
            const response = await fetch("http://localhost:8000/api/search/pois/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch points");
            }

            const data = await response.json();
            const points = data.map((point) => ({
                lat: point.latitude,
                lng: point.longitude,
            }));
            setPoints(points);
        } catch (error) {
            console.error(error);
            setPoints([]);
        }
    };

    const handleSearchInputChange = (event) => {
        setSearchValue(event.target.value);
    };


    function getMap() {
        const mapElement = document.querySelector('#map-container');
        html2canvas(mapElement).then(canvas => {
            dataUrl = canvas.toDataURL();
            console.log(dataUrl);
        });
    }
    const handleSaveSearch = async () => {
        getMap();
        try {
            const response = await fetch("http://localhost:8000/api/search/savedscreenshot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({dataUrl}),
            });

            if (!response.ok) {
                throw new Error("Failed to save screenshot");
            }

            console.log("Screenshot saved successfully");
        } catch (error) {
            console.error(error);
        }
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
                <button onClick={handleCategoriesClick}>Categories</button>
                {categories.map((category) => (
                <div key={category}>
                <input type="checkbox" value={category} onChange={handleCategoryChange} />
                <label>{category}</label>
                </div>
      ))}
                <Button variant="contained" color="primary" onClick={handleSearch}>
                    Search
                </Button>
                <Button variant="contained" color="primary" onClick={handleSaveSearch}>
                    Save Search
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
                onLoad={(map) => {
                    setMapInstance(map);
                    mapRef.current = map;
                }}
            >
                {points.map((point, index) => (
                    <MarkerF key={index} position={point}/>
                ))}
            </GoogleMap>
        </div>
    ) : null;
}

export default React.memo(Home)