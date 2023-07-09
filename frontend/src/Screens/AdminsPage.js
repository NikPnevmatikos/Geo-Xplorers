import React, { useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../App';
import axios from 'axios';

import Modal from 'react-bootstrap/Modal';
import "../Styles/Admin.css";


function AdminsPage() {

    const [pois, setPois] = useState([]);
    const [ctgs, setCtgs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useContext(UserContext);
    const navigate = useNavigate();
    const [show_ctg, setShow_ctg] = useState(false);
    const [show_poi, setShow_poi] = useState(false);
    const [file, setFile] = useState();
    const [success, setSuccess] = useState(false);

    // open and close modals, for pois and categories
    const handleClose_poi = () => setShow_poi(false);
    const handleShow_poi = () => setShow_poi(true);

    const handleClose_ctg = () => setShow_ctg(false);
    const handleShow_ctg = () => setShow_ctg(true);

    /**
    *`getPois` and `getCtgs` make API requests to retrieve points of interest 
    *and categories respectively.
    */
    async function getPois() {
        try {
            const config = {
                headers: {
                    'Content-type': 'application/json',
                    Authorization : `Bearer ${user.token}`
                }
            }
            const { data } = await axios.get(
                "http://localhost:8000/api/get/pois/",
                config
            )
            setLoading(false);
            // console.log(data);
            setPois(data);
        } catch (error) {
            setLoading(false);
            window.alert(error);
        }
    }

    async function getCtgs() {
        try {
            const config = {
                headers: {
                    'Content-type': 'application/json',
                    Authorization : `Bearer ${user.token}`
                }
            }
            const { data } = await axios.get(
                "http://localhost:8000/api/categories/",
                config
            )
            setLoading(false);
            console.log(data);
            setCtgs(data);
        } catch (error) {
            setLoading(false);
            window.alert(error);
        }
    }


    /* If the user isn't staff, the user will be navigated to the homepage. */
    useEffect(() => {
        if ((user && user.is_staff === false)) {
            navigate('/');
            console.log("user is staff bich ",user);
        }
        else if (user) {
            setLoading(true);
            getPois();
            getCtgs();

            // pop the toast notification
            if (success) {
                setSuccess(false);
            }
        }
    }, [user, success])

    const upload = (e) => {
        const file = e.target.files[0];
        setFile(file);
        // setPreview(URL.createObjectURL(file))
    }

    /**
     * The function `saveFile` is an asynchronous function that saves a file by sending a POST request
     * to a specified API endpoint, either for importing points of interest (POIs) or categories, and
     * handles success and error cases accordingly.
     * @param isPoi - isPoi is a boolean parameter that determines whether the file being saved is a
     * Point of Interest (POI) file or a category file. If isPoi is true, the file will be saved as a
     * POI file. If isPoi is false, the file will be saved as
     */
    const saveFile = async(isPoi) => {
        try {
            const form = new FormData();
            form.append('file', file); 
     
            const config = {
                headers: {
                    'Content-type': 'multipart/form-data',
                    Authorization : `Bearer ${user.token}`
                }
            }
            
            if (isPoi) {
                const { data } = await axios.post(
                    "http://localhost:8000/api/import/pois/",
                    form,
                    config
                )
            }
            else {
                const { data } = await axios.post(
                    "http://localhost:8000/api/import/categories/",
                    form,
                    config
                )
            }

            setLoading(false);

            if (isPoi) {
                handleClose_poi();
            }
            else {
                handleClose_ctg();
            }
            
            setSuccess(true);
        } 
        catch (error) {
            setLoading(false);
            console.log(error)
            window.alert(error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message);
        }
    }

    {/** 

     */}
    if (loading) {
        return <div></div>
    }

    return (
        <div>
            {/* modal for uploading categories */}

            <Modal show={show_ctg} onHide={handleClose_ctg}>
                <Modal.Header closeButton>
                    <Modal.Title>Create a new category!</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <text>Upload your file:</text>
                    <br/>
                    <input type="file" style={{padding: "4px"}} onChange={upload}/>
                </Modal.Body>
                
                <Modal.Footer>
                    <button className="admin-button-cancel" onClick={handleClose_ctg}>
                        Cancel
                    </button>
                    <button className="admin-button" onClick={() => saveFile(false)}>
                        Save Changes
                    </button>
                </Modal.Footer>
            </Modal>


            {/* modal for uploading points of interest */}

            <Modal show={show_poi} onHide={handleClose_poi}>
                <Modal.Header closeButton>
                    <Modal.Title>Create a new point of interest!</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <text>Upload your file:</text>    
                    <br/>
                    <input type="file" style={{padding: "4px"}} onChange={upload}/>
                </Modal.Body>

                <Modal.Footer>
                    <button className="admin-button-cancel" onClick={handleClose_poi}>
                        Cancel
                    </button>
                    <button className="admin-button" onClick={() => saveFile(true)}>
                        Save Changes
                    </button>
                </Modal.Footer>
            </Modal>


            
            <div className="admin-container">
                
                <div className="admin-container-head">
                    <h2 className="admin-title">
                        My Admin's Page
                    </h2>
                    <button className="admin-button" onClick={handleShow_ctg}>
                        Upload <strong>New Category</strong>
                    </button>
                    <button className="admin-button" onClick={handleShow_poi}>
                        Upload <strong>New POI</strong>
                    </button>            
                </div>


                <div class="container" className="admin-container-table">
                    <div class="row">
                        <div class="col" className="admin-table-col" style={{width: "70%"}}>
                            <h5>Points of Interest:</h5>
                            <div class="col" className="admin-table">
                                <table class="table table-striped table-hover">
                                    <thead>
                                        <tr>    
                                            <th scope="col"><strong>Title</strong></th>
                                            <th scope="col"><strong>lat-lng</strong></th>
                                            <th scope="col"><strong>Categories</strong></th>
                                            <th scope="col"><strong>Keywords</strong></th>
                                        </tr>
                                    </thead>
                                    <tbody className="admin-table">
                                        {(!loading && pois && pois.length > 0) ?
                                            pois.map((poi) => {
                                                return(
                                                    <tr key={poi._id}>
                                                        <th scope="row">{poi.title}</th>
                                                        <td>{poi.latitude}, {poi.longitude}</td>
                                                        <td>
                                                            {poi.categories.map((category, index)=> {
                                                                const isLastElement = index === poi.categories.length - 1;
                                                                const comma = isLastElement ? '' : ', ';
                                                                return <text>{category.name}{comma}</text>;
                                                            })}
                                                        </td>
                                                        <td>
                                                            {poi.keywords.map((keyword, index)=> {
                                                                const isLastElement = index === poi.keywords.length - 1;
                                                                const comma = isLastElement ? '' : ', ';
                                                                return <text>{keyword.keyword}{comma}</text>;
                                                            })}</td>
                                                    </tr>
                                                )
                                            })
                                        :
                                            null
                                        }
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        
                        <div class="col" style={{width: "40%"}}>
                            <h5>Categories:</h5>
                            <div class="col-3" className="admin-table">
                                
                                <table class="table table-striped table-hover">
                                    <thead>
                                        <tr>    
                                            <th scope="col"><strong>Name</strong></th>
                                        </tr>
                                    </thead>
                                    <tbody className="admin-table">
                                        {(!loading && ctgs && ctgs.length > 0) ?
                                            ctgs.map((ctg) => {
                                                return(
                                                    <tr key={ctg._id}>
                                                        <th scope="row">{ctg.name}</th>
                                                        {/* <td>{poi.latitude}, {poi.longitude}</td>
                                                        <td>
                                                            {poi.categories.map((category, index)=> {
                                                                const isLastElement = index === poi.categories.length - 1;
                                                                const comma = isLastElement ? '' : ', ';
                                                                return <text>{category.name}{comma}</text>;
                                                            })}
                                                        </td>
                                                        <td>
                                                            {poi.keywords.map((keyword, index)=> {
                                                                const isLastElement = index === poi.keywords.length - 1;
                                                                const comma = isLastElement ? '' : ', ';
                                                                return <text>{keyword.keyword}{comma}</text>;
                                                            })}</td> */}
                                                    </tr>
                                                )
                                            })
                                        :
                                            null
                                        }
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        
                        
                    </div>
                </div>

            </div>        
        </div>
    )
}

export default AdminsPage