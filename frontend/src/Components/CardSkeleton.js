import React from 'react';
import './SaveSearches.css';
import { Grid, Card, CardContent, CardMedia, Typography, Skeleton, CardActions, CardHeader } from '@mui/material';

const CardSkeleton = ({ cards }) => {
    // Function to render the skeleton cards
    const renderCardSkeletons = () => {
        return Array(cards)
            .fill(0)
            .map((item, index) => (
                <Grid key={index} item xs={12}>
                    {/* Skeleton card */}
                    <Card sx={{ minWidth: 800, maxWidth: 800, maxHeight: 250, minHeight: 250, backgroundColor: 'white', boxShadow: '5px 10px 10px rgba(2, 128, 144, 0.2)', borderRadius: '20px' }} className="card">
                        <CardHeader sx={{ height: '7px', padding: '8px' }} />
                        <div className="card_action_area_container">
                            <div className="card_img">
                                {/* Skeleton image */}
                                <Skeleton variant="rectangular" height={170} width={300} />
                            </div>
                            <div className="text_button_container">
                                <CardContent className="text_container">
                                    <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-line', fontSize: '16px' }}>
                                        {/* Skeleton text */}
                                        <Skeleton style={{ width: '400px' }} />
                                        <Skeleton />
                                        <Skeleton />
                                        <Skeleton />
                                    </Typography>
                                </CardContent>

                                {/* Skeleton card actions */}
                                <CardActions style={{ marginTop: 'auto' }}>
                                    <Skeleton style={{ padding: '10px 20px', width: '200px' }} />
                                </CardActions>
                            </div>
                        </div>
                    </Card>
                </Grid>
            ));
    };

    return (
        <Grid container spacing={4} direction="column" justifyContent="center" alignItems="center">
            {/* Render the skeleton cards */}
            {renderCardSkeletons()}
        </Grid>
    );
};

export default CardSkeleton;