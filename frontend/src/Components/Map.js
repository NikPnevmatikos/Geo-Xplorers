import React, {
  useState,
  useEffect,
  useRef,
  createRef,
  useContext,
} from "react";
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
import { IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { UserContext } from "../App";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function Map(props) {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    // googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    googleMapsApiKey: "AIzaSyBZ1a96JQbH-jmgz79ItO2cGlIxv2luZNI"
  });

  const {
    visible,
    radius,
    setRadius,
    circleCenter,
    setCircleCenter,
    mapAction,
    setSelectedCategories,
    selectedCategories,
    selectedKeywords,
    setSelectedKeywords,
    setMapAction,
  } = props;
  const location = useLocation();
  const navigate = useNavigate();
  const [mapInstance, setMapInstance] = useState(null);
  const [searchValue, setSearchValue] = useState("");
  const [points, setPoints] = useState([]);
  const [metadata, setMetadata] = useState([]);
  const mapRef = useRef(null);
  const ref = createRef(null);
  const [image, takeScreenshot] = useScreenshot();
  const getImage = () => takeScreenshot(ref.current);
  const [categories, setCategories] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const circleRef = useRef(null);
  const [circleInstance, setCircleInstance] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: 37.98381, lng: 23.727539 });
  const [user, setUser] = useContext(UserContext);

  const handleRadiusChange = (event) => {
    setRadius(parseInt(event.target.value, 10)); // Update the radius value
  };

  //TO CHANGE MAYBE
  useEffect(() => {
    if (mapAction) {
      handleModalOpen();
    }
  }, [mapAction]);

  const handleMapDrag = () => {
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
  let radlat = params.get("lat");
  let radlng = params.get("lng");
  let radkm = params.get("km");

  useEffect(() => {
    if (
      (text && text !== "") ||
      (catParam && catParam != "") ||
      (keywordParam && keywordParam != "") ||
      (radlat && radlat != "" && radlng && radlng != "" && radkm && radkm != "")
    ) {
      apiSearch();
    }
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
      let selectedDistance = {};
      if (
        radlat &&
        radlat != "" &&
        radlng &&
        radlng != "" &&
        radkm &&
        radkm != ""
      ) {
        selectedDistance = {
          lat: Number(radlat),
          lng: Number(radlng),
          km: parseInt(radkm / 1000),
        };
      }

      const requestBody = {
        filters: {
          categories: selected,
          keywords: selectedKey,
          distance: selectedDistance,
        },
        text: text,
      };
      let config = {
        headers: {
          "Content-type": "application/json",
        },
      };

      if (user) {
        config = {
          headers: {
            "Content-type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
        };
      }

      const { data } = await axios.post(
        "http://localhost:8000/api/search/pois/",
        requestBody,
        config
      );

      const response = data.data;
      //map every object of the response list to a point inside the points array keeping only latitude and longitude
      const points = response.map((point) => ({
        lat: Number(point.latitude),
        lng: Number(point.longitude),
        title: point.title,
        description: point.description,
      }));
      setPoints(points);
      if (response.length === 0) {
        toast("No results found", { type: "error" });
        console.log("No results found");
      }
    } catch (error) {
      setPoints([]);
    }
  }

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
          Authorization: `Bearer ${user.token}`,
        },
      };

      const { data } = await axios.post(
        "http://localhost:8000/api/search/image/30/",
        form,
        config
      );
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
    setMapAction(false);
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
      <Modal
        open={modalOpen}
        onClose={handleModalClose}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            backgroundColor: "#f2f2f2",
            width: "35%",
            height: "50%",
            borderRadius: "8px",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <IconButton
            style={{ alignSelf: "flex-end" }}
            onClick={handleModalClose}
          >
            <CloseIcon />
          </IconButton>
          <h3 style={{ marginTop: -10, marginBottom: "20px" }}>
            Choose Filters
          </h3>
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
          options={{
            mapTypeControl: true, // Enable map type control
            mapTypeControlOptions: {
              position: window.google.maps.ControlPosition.BOTTOM_CENTER, // Set position of map type controls
            },
            fullscreenControl: false, // Remove fullscreen button
          }}
        >
          <ToastContainer />
          {points.map((point, index) => (
            <MarkerF
              key={index}
              position={{ lat: point.lat, lng: point.lng }}
              title={point.description}
              label={point.title}
            />
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
              }}
            />
          )}
        </GoogleMap>
      </div>
    </div>
  ) : null;
}

export default React.memo(Map);
