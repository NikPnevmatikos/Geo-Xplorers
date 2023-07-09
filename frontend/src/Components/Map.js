import React, { useState, useEffect, useRef, createRef } from "react";
import {
  GoogleMap,
  Marker,
  MarkerF,
  useJsApiLoader,
  Circle,
} from "@react-google-maps/api";
import { useLocation, useNavigate } from "react-router-dom";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useScreenshot } from "use-react-screenshot";
import { Button } from "@mui/material";
import { Modal } from "@mui/material";
import { FormControlLabel } from "@mui/material";
import { Checkbox } from "@mui/material";
import { FormGroup } from "@mui/material";
import { InputAdornment } from "@mui/material";

function Map(props) {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  const { visible, radius, setRadius, circleCenter, setCircleCenter } = props;
  const location = useLocation();
  const navigate = useNavigate();
  const [mapInstance, setMapInstance] = useState(null);
  const [searchValue, setSearchValue] = useState("");
  const [points, setPoints] = useState([]);
  const mapRef = useRef(null);
  const ref = createRef(null);
  const [image, takeScreenshot] = useScreenshot();
  const getImage = () => takeScreenshot(ref.current);
  const [categories, setCategories] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedKeywords, setSelectedKeywords] = useState([]);

  const circleRef = useRef(null);
  const [circleInstance, setCircleInstance] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: 37.98381, lng: 23.727539 });

  const handleRadiusChange = (event) => {
    setRadius(parseInt(event.target.value, 10)); // Update the radius value
  };

  const handleMapDrag = () => {
    console.log(mapRef.current);
    const newCenter = {
      lat: mapRef.current.getCenter().lat(),
      lng: mapRef.current.getCenter().lng(),
    };
    setMapCenter(newCenter);
    setCircleCenter(newCenter);
  };

  const handleCenterChanged = () => {
    if (circleInstance) {
      const newCenter = {
        lat: circleInstance["center"].lat(),
        lng: circleInstance["center"].lng(),
      };

      setCircleCenter(newCenter);
    }
  };

  useEffect(() => {
    if (mapInstance && points.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      points.forEach((point) => bounds.extend(point));
      mapInstance.fitBounds(bounds);
    }
  }, [mapInstance, points, image]);

  async function getCategories() {
    await axios
      .get("http://localhost:8000/api/categories/")
      .then((response) => {
        setCategories(response.data);
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }
  useEffect(() => {
    getCategories();
  }, []);

  const handleKeywordsChange = (event) => {
    setSelectedKeywords(event.target.value);
  };

  const params = new URLSearchParams(location.search);
  let text = params.get("text");
  let catParam = params.get("categories");
  let keywordParam = params.get("keywords");
  useEffect(() => {
    if (
      (text && text !== "") ||
      (catParam && catParam != "") ||
      (keywordParam && keywordParam != "")
    ) {
      console.log("mpika");
      apiSearch();
    }
    console.log(text);
  }, [text, catParam, keywordParam]);

  async function apiSearch() {
    try {
      let selected = [];
      let selectedKey = [];
      if (catParam && catParam != "") {
        selected = catParam.split(",");
      }
      if (keywordParam && keywordParam != "") {
        selectedKey = keywordParam.split(",");
      }

      const requestBody = {
        filters: {
          categories: selected,
          keywords: selectedKey,
          distance: {},
        },
        text: text,
      };
      const config = {
        headers: {
          "Content-type": "application/json",
        },
      };

      const { data } = await axios.post(
        "http://localhost:8000/api/search/pois/",
        requestBody,
        config
      );

      const response = data.data;
      console.log(response);
      //map every object of the response list to a point inside the points array keeping only latitude and longitude
      const points = response.map((point) => ({
        lat: Number(point.latitude),
        lng: Number(point.longitude),
      }));
      console.log(Number(response[0].latitude));
      setPoints(points);
      console.log(points);
    } catch (error) {
      alert(error);
      setPoints([]);
    }
  }

  //SEARCH BUTTON FUNCTIONALITY
  const handleSearch = () => {
    if (
      searchValue != "" ||
      selectedCategories.length > 0 ||
      selectedKeywords.length > 0
    ) {
      const cat = selectedCategories.toString();
      const keywords = selectedKeywords.toString();
      navigate(`/?text=${searchValue}&categories=${cat}&keywords=${keywords}`);
    } else {
      setPoints([]);
      navigate(`/`);
    }
  };

  const handleSearchInputChange = (event) => {
    setSearchValue(event.target.value);
  };

  //SAVE SEARCH BUTTON FUNCTIONALITY
  const handleSaveSearch = async () => {
    try {
      // const newImg = await convertImageToBinary(image)
      const form = new FormData();
      form.append("image", image);

      const config = {
        headers: {
          "Content-type": "multipart/form-data",
          Authorization:
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzOTQzNjc5LCJpYXQiOjE2ODg3NTk2NzksImp0aSI6ImRlNTFhZjRjNmFiMjQzZDA4Yzg0ODViNTI2YTcxYjRiIiwidXNlcl9pZCI6MX0.e7fKrTF3K78IUaGWQ_-lMltKh9yNNt8FiJJcM4J5kL0",
        },
      };

      const { data } = await axios.post(
        "http://localhost:8000/api/search/image/30/",
        form,
        config
      );
      console.log(data);
      console.log("Screenshot saved successfully");
    } catch (error) {
      console.error(error);
    }
  };

  //   //MODAL FUNCTIONALITY
  const handleModalOpen = () => {
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    console.log(selectedCategories);
    console.log(selectedKeywords);
  };

  const handleCategoryChange = (event) => {
    const categoryName = event.target.name;
    const isChecked = event.target.checked;

    if (isChecked) {
      setSelectedCategories([...selectedCategories, categoryName]);
    } else {
      setSelectedCategories(
        selectedCategories.filter((category) => category !== categoryName)
      );
    }
  };

  return isLoaded ? (
    <div>
      <div
        style={{
          marginTop: 80,
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-end",
          padding: "10px",
          backgroundColor: "#8ab4f8",
        }}
      >
        <TextField
          type="text"
          value={searchValue}
          onChange={handleSearchInputChange}
          label="Search"
          variant="outlined"
          style={{ marginRight: "10px" }}
        />
        <Button variant="contained" color="primary" onClick={handleModalOpen}>
          Filters
        </Button>
        <Modal
          open={modalOpen}
          onClose={handleModalClose}
          aria-labelledby="modal-title"
          aria-describedby="modal-description"
          sx={{
            display: "flex",
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "white",
            width: "35%",
            height: "50%",
          }}
        >
          <div>
            <FormGroup>
              {categories.map((category) => (
                <FormControlLabel
                  key={category.id}
                  control={
                    <Checkbox
                      checked={selectedCategories.includes(category.name)}
                      onChange={handleCategoryChange}
                      name={category.name}
                    />
                  }
                  label={category.name}
                />
              ))}
            </FormGroup>
            <TextField
              type="text"
              label="Keywords (separated by commas)"
              variant="outlined"
              style={{ marginTop: "10px" }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">Keywords</InputAdornment>
                ),
              }}
              value={selectedKeywords}
              onChange={handleKeywordsChange}
            />
          </div>
        </Modal>
        <Button variant="contained" color="primary" onClick={handleSearch}>
          Search
        </Button>
        <Button variant="contained" color="primary" onClick={handleSaveSearch}>
          Save Search
        </Button>
      </div>
      <div ref={ref}>
        <GoogleMap
          id="map"
          mapContainerStyle={{
            width: "100%",
            height: "100vh",
          }}
          center={mapCenter}
          onDragEnd={handleMapDrag}
          zoom={10}
          onLoad={(map) => {
            setMapInstance(map);
            mapRef.current = map;
          }}
        >
          {points.map((point, index) => (
            <MarkerF key={index} position={point} />
          ))}
          {visible === true && (
            <Circle
              center={mapCenter} // Set the center point of the circle
              radius={radius} // Set the radius value dynamically
              onCenterChanged={() => handleCenterChanged()}
              onRadiusChanged={() =>
                circleInstance && setRadius(parseInt(circleInstance["radius"]))
              }
              onLoad={(circle) => {
                setCircleInstance(circle);
                circleRef.current = circle;
              }}
              onUnmount={(circle) => setCircleInstance(null)}
              options={{
                fillColor: "blue",
                fillOpacity: 0.3,
                strokeWeight: 1,
                strokeOpacity: 0,
                editable: true,
              }} // Customize the circle's appearance
            />
          )}
        </GoogleMap>
      </div>
      {/* <img src={image} alt="screenshot" /> */}
    </div>
  ) : null;
}

export default React.memo(Map);
