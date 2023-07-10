import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios from "axios";
import {
  Card,
  CardActionArea,
  Grid,
  CardMedia,
  Typography,
  CardContent,
  CardActions,
  Button,
  CardHeader,
  IconButton,
  Modal,
  Box,
} from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faTrash } from "@fortawesome/free-solid-svg-icons";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useNavigate } from "react-router-dom";
import "./SaveSearches.css";
import CardSkeleton from "./CardSkeleton";

const MAX_TEXT_SIZE = 150; // The maximum text size which is displayed in the card

export default function Save_Searches() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedItemIds, setExpandedItemIds] = useState([]);
  const [deleted, setDeleted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItemId, setSelectedItemId] = useState(null);
  const [user, setUser] = useContext(UserContext);
  const navigate = useNavigate();

  // Function to expand the item text
  const handleShowMore = (itemId) => {
    setExpandedItemIds((prevExpandedItemIds) => [
      ...prevExpandedItemIds,
      itemId,
    ]);
  };

  // Function to collapse the item text
  const handleShowLess = (itemId) => {
    setExpandedItemIds((prevExpandedItemIds) =>
      prevExpandedItemIds.filter((_id) => _id !== itemId)
    );
  };

  // Function to handle delete button click
  const handleDeleteClick = (id) => {
    setDeleted(false);
    setSelectedItemId(id);
    setIsOpen(true);
  };

  // Function to delete an item
  const handleDelete = (id) => {
    setIsOpen(false);
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const config = {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
        };
        const response = await axios.delete(
          `http://localhost:8000/api/searches/?pk=${selectedItemId}`,
          config
        );

        const responseData = response.data;

        console.log(responseData);
        setData(responseData);
        setDeleted(true);
        console.log("Deleted successfully");
        toast.success("Deleted successfully", {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "light",
        });
      } catch (error) {
        console.error("Error deleting:", error);
      }
    };

    fetchData();
  };

  // Function to navigate to item details
  const navigateToItem = (itemId) => {
    navigate(`/?id=${itemId}`);
  };

  // Style for the modal
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    p: 2,
    borderRadius: "9px",
  };

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const config = {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
        };
        const response = await axios.get(
          "http://localhost:8000/api/searches/?type=saved",
          config
        );

        const responseData = response.data;

        console.log(responseData);
        setData(responseData);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching saved searches data:", error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, [deleted, user]);

  const totalItems = 2;

  return (
    <div>
      {/* Heading */}
      <br />
      <h3 style={{ marginTop: "90px", textAlign: "center" }}>Saved Searches</h3>
      <br />

      {/* No searches message */}
      {!isLoading && data.length === 0 && (
        <div>
          <h5 style={{ marginTop: "70px", textAlign: "center" }}>
            No searches yet!
          </h5>
          <br />
          <div className="img_no_searches_container">
            <img src="/no_searches.jpg" className="img_no_searches" />
          </div>
        </div>
      )}

      <Grid
        container
        spacing={4}
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        {isLoading ? (
          // Skeleton card when loading
          <CardSkeleton cards={totalItems} />
        ) : (
          // Render saved search cards
          data.map((item) => (
            <Grid item xs={12} key={item._id}>
              <Card
                sx={{
                  minWidth: 800,
                  maxWidth: 800,
                  maxHeight: 250,
                  minHeight: 250,
                  backgroundColor: "white",
                  boxShadow: "5px 10px 10px rgba(2, 128, 144, 0.2)",
                  borderRadius: "20px",
                }}
                className="card"
              >
                <CardHeader
                  sx={{ height: "7px", padding: "8px" }}
                  onClick={() => handleDeleteClick(item._id)}
                  action={
                    <IconButton
                      aria-label="settings"
                      sx={{
                        position: "relative",
                        "&:hover": {
                          background: "rgba(255, 0, 0, 0.1)",
                        },
                      }}
                    >
                      <FontAwesomeIcon
                        icon={faTrash}
                        style={{
                          color: "red",
                          width: "16px",
                          padding: "0 8px",
                        }}
                      />
                    </IconButton>
                  }
                />

                {/* Modal for delete confirmation */}
                <Modal open={isOpen} onClose={() => setIsOpen(false)}>
                  <Box sx={style}>
                    <FontAwesomeIcon
                      icon={faTimes}
                      size="lg"
                      onClick={() => setIsOpen(false)}
                      className="close-icon "
                    />
                    <br />
                    <br />
                    <h5 id="parent-modal-title" style={{ textAlign: "center" }}>
                      Are you sure you want to delete that?
                    </h5>
                    <br />
                    <button
                      className="admin-button"
                      onClick={() => handleDelete(item._id)}
                    >
                      Yes Delete
                    </button>
                    <button
                      className="admin-button-cancel"
                      onClick={() => setIsOpen(false)}
                    >
                      Cancel
                    </button>
                  </Box>
                </Modal>

                {/* Card content */}
                <div className="card_action_area_container">
                  <CardActionArea
                    style={{ width: "300px", marginRight: "1rem" }}
                    onClick={() => navigateToItem(item._id)}
                  >
                    <CardMedia
                      key={item._id}
                      component="img"
                      className="card_img"
                      sx={{ width: 300, height: 170 }}
                      image={`http://localhost:8000${item.image}`}
                      alt="Image Alt Text"
                    />
                  </CardActionArea>
                  <div className="text_button_container">
                    <CardContent className="text_container">
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                          whiteSpace: "pre-line",
                          fontSize: "16px",
                          color: "black",
                        }}
                      >
                        {(() => {
                          const displayString = [
                            item.text !== null ? `${item.text}` : "",
                            item.categories !== null &&
                            item.categories.length > 0
                              ? `Categories:${item.categories
                                  .map((category) => category.name)
                                  .join(",")}`
                              : "",
                            item.keywords !== null && item.keywords.length > 0
                              ? `Keywords:${item.keywords
                                  .map((keyword) => keyword.keyword)
                                  .join(",")}`
                              : "",
                            item.latitude !== null
                              ? `Latitude: ${item.latitude}`
                              : "",
                            item.longitude !== null
                              ? `Longitude: ${item.longitude}`
                              : "",
                            item.kilometers !== null
                              ? `Kilometers: ${item.kilometers}`
                              : "",
                          ]
                            .filter(Boolean)
                            .join("\n");

                          const shouldShowMoreButton =
                            displayString.length > MAX_TEXT_SIZE;
                          const isExpanded = expandedItemIds.includes(item._id);

                          if (displayString) {
                            return (
                              <>
                                {!isExpanded && (
                                  <>
                                    {shouldShowMoreButton ? (
                                      <>
                                        {displayString.substring(
                                          0,
                                          MAX_TEXT_SIZE
                                        )}
                                        ...
                                        <Button
                                          onClick={() =>
                                            handleShowMore(item._id)
                                          }
                                          style={{
                                            fontSize: "13px",
                                            textTransform: "lowercase",
                                          }}
                                          className="button_showMore_showLess"
                                        >
                                          Show more
                                        </Button>
                                      </>
                                    ) : (
                                      <>{displayString}</>
                                    )}
                                  </>
                                )}
                                {isExpanded && (
                                  <>
                                    {displayString}
                                    <br />
                                    <Button
                                      onClick={() => handleShowLess(item._id)}
                                      style={{
                                        fontSize: "13px",
                                        textTransform: "lowercase",
                                      }}
                                      className="button_showMore_showLess"
                                    >
                                      Show Less
                                    </Button>
                                  </>
                                )}
                              </>
                            );
                          } else {
                            return null;
                          }
                        })()}
                      </Typography>
                    </CardContent>

                    {/* Card actions */}
                    <CardActions
                      style={{ marginTop: "auto" }}
                      className="fixed_button"
                    >
                      {item.newPois === 0 ? (
                        <CardActionArea
                          onClick={() => navigateToItem(item._id)}
                          sx={{ width: "270px" }}
                        >
                          <a className="notification">Points of interest</a>
                        </CardActionArea>
                      ) : (
                        <CardActionArea
                          onClick={() => navigateToItem(item._id)}
                          sx={{ width: "270px" }}
                        >
                          <a className="notification">
                            <span>New points of interest</span>
                            <span className="badge">{item.newPois}</span>
                          </a>
                        </CardActionArea>
                      )}
                    </CardActions>
                  </div>
                </div>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
      <ToastContainer />
    </div>
  );
}
