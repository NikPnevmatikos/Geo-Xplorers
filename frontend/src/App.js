import React, { createContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SaveSearches from "./Components/SaveSearches";
import './bootstrap.min.css';
import HomeScreen from './Screens/HomeScreen';
import LoginScreen from './Screens/LoginScreen';
import RegisterScreen from './Screens/RegisterScreen';
import Header from './Components/Header';
import AdminsPage from './Screens/AdminsPage';

//create a context, with createContext api
export const UserContext = createContext();


function App() {

    // this state will be shared with all components 
    const [user, setUser] = useState();

    //useEffect pou 8a koitaei to local storage kai an uparxei, setUser
    useEffect(() => {
        const user = localStorage.getItem("User");
        if (user !== null) {
            setUser(JSON.parse(user));
        }
    }, []);


    //useEffect pou 8a koitaei to local storage kai an uparxei, setUser
    useEffect(() => {
        console.log(user);
    }, [user]);

    return (
        <div className="layout">
            <UserContext.Provider value={[user, setUser]}>
                <Router>
                    <Header/>
                    <Routes>
                        <Route path="/" element={<HomeScreen/>} /> 
                        <Route path="/login/" element={<LoginScreen/>} /> 
                        <Route path="/register/" element={<RegisterScreen/>} />
                        <Route path="/admin_page/" element={<AdminsPage/>} />
                    </Routes>
                </Router>                
            </UserContext.Provider> 
        </div>
    );
}

export default App;