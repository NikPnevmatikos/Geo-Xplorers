import React, { createContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import './bootstrap.min.css';
import HomeScreen from './Screens/HomeScreen';
import LoginScreen from './Screens/LoginScreen';
import RegisterScreen from './Screens/RegisterScreen';
import Header from './Components/Header';
//import AdminsPage from './Screens/AdminsPage';

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
                        {/* <Route path="/admin_page/" element={<AdminsPage/>} /> */}
                    </Routes>
                </Router>                
            </UserContext.Provider> 
        </div>
    );
}

export default App;








// const [activeTab, setActiveTab] = useState(1);

// const handleTabClick = (tabIndex) => {
//   setActiveTab(tabIndex);
// };
    //     // <div>
    //         {/* Buttons
    //         <button className="button">Button</button>
    //         <button className="button">Button</button>
    //         <button className="button">Button</button>

    //         Forms 
    //         <div className="form-container">
    //             <div className="form-group">
    //             <label className="form-label">Name:</label>
    //             <input type="text" className="form-input" />
    //             </div>
    //             <div className="form-group">
    //             <label className="form-label">Email:</label>
    //             <input type="email" className="form-input" />
    //             </div>
    //             <div className="form-group">
    //             <label className="form-label">Password:</label>
    //             <input type="password" className="form-input" />
    //             </div>
    //             <button className="button">Submit</button>
    //         </div>

    //         Tabs
    //         <div className="tab-container">
    //             <div className="tab-header">
    //             <button
    //                 className={`tab-button ${activeTab === 1 ? 'active' : ''}`}
    //                 onClick={() => handleTabClick(1)}
    //             >
    //                 Tab 1
    //             </button>
    //             <button
    //                 className={`tab-button ${activeTab === 2 ? 'active' : ''}`}
    //                 onClick={() => handleTabClick(2)}
    //             >
    //                 Tab 2
    //             </button>
    //             <button
    //                 className={`tab-button ${activeTab === 3 ? 'active' : ''}`}
    //                 onClick={() => handleTabClick(3)}
    //             >
    //                 Tab 3
    //             </button>
    //             </div>
    //             <div className="tab-content">
    //             <div className={`tab-pane ${activeTab === 1 ? 'active' : ''}`}>
    //                 Tab 1 content
    //             </div>
    //             <div className={`tab-pane ${activeTab === 2 ? 'active' : ''}`}>
    //                 Tab 2 content
    //             </div>
    //             <div className={`tab-pane ${activeTab === 3 ? 'active' : ''}`}>
    //                 Tab 3 content
    //             </div>
    //             </div>
    //         </div>
    //         <div className="card">
    //             <h2 className="card-title">Card Title</h2>
    //             <p className="card-content">
    //                 This is the content of the card. You can add any text or other elements here.
    //             </p>
    //             <div className="card-actions">
    //                 <button className="card-button">Action 1</button>
    //                 <button className="card-button">Action 2</button>
    //             </div>
    //         </div>
    // </div> */}
