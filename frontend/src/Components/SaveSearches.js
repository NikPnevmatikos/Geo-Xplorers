import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardActionArea, Grid, CardMedia, Typography, CardContent, CardActions, Button, CardHeader, IconButton, Modal, Box, ChildModal } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './SaveSearches.css';
import { useNavigate } from 'react-router-dom';
import CardSkeleton from './CardSkeleton';
import { grey } from '@mui/material/colors';

// import CardSkeleton from './CardSkeleton';
const MAX_TEXT_SIZE = 100; // Set the maximum text size here

export default function Save_Searches() {

    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [expandedItemIds, setExpandedItemIds] = useState([]);
    const [deleted, setDeleted] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const [selectedItemId, setSelectedItemId] = useState(null);

    const handleShowMore = (itemId) => {
        setExpandedItemIds((prevExpandedItemIds) => [...prevExpandedItemIds, itemId]);
    };

    const handleShowLess = (itemId) => {
        setExpandedItemIds((prevExpandedItemIds) => prevExpandedItemIds.filter((_id) => _id !== itemId));
    };

    const handleDeleteClick = (id) => {
        setDeleted(false);
        setSelectedItemId(id);
        setIsOpen(true);
    };

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 350,
        bgcolor: 'background.paper',
        p: 4,
        borderRadius:'9px'
    };


    const handleDelete = (id) => {
        // Perform the delete action here
        setIsOpen(false);
        // const updatedData = data.filter((item) => item._id !== selectedItemId);
        // setData(updatedData);
        axios
            .delete(`http://localhost:8000/api/searches/?pk=${selectedItemId}`, {
                headers: {
                    Authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzODU3ODE2LCJpYXQiOjE2ODg2NzM4MTYsImp0aSI6ImE3MGQ3OGMzNmYzOTQyMTNiNzYxNGUxZTE0NzdkNDFmIiwidXNlcl9pZCI6Mn0.QJpT6Vtp9d_B6G7f4chz34k_dJYWk-ILc9fvLQf5IjQ',
                    'Content-Type': 'application/json',
                },
            })
            .then(() => {
                setDeleted(true);
                console.log('Deleted successfully');
                toast.success('Deleted successfully', {
                    position: "top-right",
                    autoClose: 2000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                    color:"red"
                });
            })
            .catch((error) => {
                console.error('Error deleting:', error);
            });
    };

    const navigate = useNavigate();

    const navigateToItem = (itemId) => {
        // Replace "/path-to-item/:itemId" with the actual path of your item detail page
        navigate(`/path-to-item/${itemId}`);
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const config = {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzODU3ODE2LCJpYXQiOjE2ODg2NzM4MTYsImp0aSI6ImE3MGQ3OGMzNmYzOTQyMTNiNzYxNGUxZTE0NzdkNDFmIiwidXNlcl9pZCI6Mn0.QJpT6Vtp9d_B6G7f4chz34k_dJYWk-ILc9fvLQf5IjQ',
                    },
                };

                const response = await axios.get('http://localhost:8000/api/searches/?type=saved', config);

                const responseData = response.data;

                console.log(responseData);
                setData(responseData);
                setIsLoading(false); // Update the loading state to false
            } catch (error) {
                console.error('Error fetching data:', error);
                setIsLoading(false); // Update the loading state to false in case of an error
            }
        };

        fetchData();
    }, [deleted]);

    const totalItems = data.length;
    return (
        <div>
            <h2>Save Searches</h2><br />

            <Grid container spacing={4} direction="column" justifyContent="center" alignItems="center">

                {/* {data.length === 0 ? (
                    <h5>No searches found.</h5>
                ) : ( */}
                {isLoading ? (
                    // Render the skeleton card when isLoading is true

                    <CardSkeleton cards={totalItems} />

                ) : (
                    data.map((item) => (
                        <Grid item xs={12} key={item._id}>
                            <Card sx={{ minWidth: 800, maxWidth: 800, maxHeight: 250, minHeight: 250, backgroundColor: 'white', boxShadow: '5px 10px 10px rgba(2, 128, 144, 0.2)', borderRadius: '20px' }} className="card">
                                <CardHeader
                                    sx={{ height: '7px', padding: '8px' }}
                                    onClick={() => handleDeleteClick(item._id)}
                                    action={
                                        <IconButton aria-label="settings"
                                            sx={{
                                                position: 'relative',
                                                '&:hover': {
                                                    background: 'rgba(255, 0, 0, 0.1)',

                                                },

                                            }}>
                                            <FontAwesomeIcon icon={faTrash} style={{ color: 'red', width: '16px', padding: '0 8px', }} />
                                        </IconButton>
                                    }
                                />

                                <Modal open={isOpen} onClose={() => setIsOpen(false)}>
                                    <Box sx={style}>

                                        <FontAwesomeIcon icon={faTimes} size="lg" onClick={() => setIsOpen(false)}
                                            className="close-icon " /> <br /><br />

                                        <h3 id="parent-modal-title" style={{ textAlign: 'center' }}>Are you sure you want to delete that?</h3>
                                        <br />
                                        <button className="admin-button" onClick={() => handleDelete(item._id)}>
                                            Yes Delete
                                        </button>
                                        <button className="admin-button-cancel" onClick={() => setIsOpen(false)}>
                                            Cancel
                                        </button>
                                    </Box>
                                </Modal>

                                <div className="card_action_area_container">
                                    <CardActionArea style={{ width: '300px', marginRight: '1rem'}} onClick={() => navigateToItem(item._id)}>
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
                                            <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-line', fontSize: '16px' }}>
                                                {(() => {
                                                    const displayString = [
                                                        item.text !== null ? `${item.text}` : "",
                                                        item.categories !== null && item.categories.length > 0
                                                            ? `Categories:${item.categories.map((category) => category.name).join(",")}`
                                                            : "",
                                                        item.keywords !== null && item.keywords.length > 0
                                                            ? `Keywords:${item.keywords.map((keyword) => keyword.keyword).join(",")}`
                                                            : "",
                                                        item.latitude !== null ? `Latitude: ${item.latitude}` : "",
                                                        item.longitude !== null ? `Longitude: ${item.longitude}` : "",
                                                        item.kilometers !== null ? `Kilometers: ${item.kilometers}` : "",
                                                    ].filter(Boolean).join("\n");


                                                    const shouldShowMoreButton = displayString.length > MAX_TEXT_SIZE;
                                                    const isExpanded = expandedItemIds.includes(item._id);

                                                    if (displayString) {
                                                        return (
                                                            <>
                                                                {!isExpanded && (
                                                                    <>
                                                                        {shouldShowMoreButton ? (
                                                                            <>
                                                                                {displayString.substring(0, MAX_TEXT_SIZE)}...
                                                                                <Button onClick={() => handleShowMore(item._id)} style={{ fontSize: '13px', textTransform: 'lowercase' }} className='button_showMore_showLess'>Show more </Button>
                                                                            </>
                                                                        ) : (
                                                                            <>
                                                                                {displayString}
                                                                            </>
                                                                        )}
                                                                    </>
                                                                )}
                                                                {isExpanded && (
                                                                    <>
                                                                        {displayString}
                                                                        <br />
                                                                        <Button onClick={() => handleShowLess(item._id)} style={{ fontSize: '13px', textTransform: 'lowercase' }} className='button_showMore_showLess'>Show Less</Button>
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

                                        <CardActions style={{ marginTop: 'auto' }} className="fixed_button">
                                            {item.newPois === 0 ? (
                                                <CardActionArea onClick={() => navigateToItem(item._id)} sx={{ width: '240px' }}>
                                                    <a className="notification">
                                                        Points of interest
                                                    </a>
                                                </CardActionArea>
                                            ) : (
                                                <CardActionArea onClick={() => navigateToItem(item._id)} sx={{ width: '240px' }}>
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

                {/* )} */}


            </Grid>
            <ToastContainer />
        </div>
    );
}