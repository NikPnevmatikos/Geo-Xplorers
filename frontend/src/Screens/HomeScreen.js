import React from 'react'
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Map from "../Components/Map";
import Header from '../Components/Header';

function HomeScreen() {
  return (
    <div>
        <Header/>
        <Router>
            <Routes>
                <Route path="" element={<Map/>}/>
            </Routes>
        </Router>    
    </div>
  )
}

export default HomeScreen