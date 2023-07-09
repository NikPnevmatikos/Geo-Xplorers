import React, { createContext, useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import "./bootstrap.min.css";
import HomeScreen from "./Screens/HomeScreen";
import LoginScreen from "./Screens/LoginScreen";
import RegisterScreen from "./Screens/RegisterScreen";
import Header from "./Components/Header";
import AdminsPage from "./Screens/AdminsPage";
import SaveSearches from "./Components/SaveSearches";
import NotBell from "./Components/NotBell";


//create a context, with createContext api
export const UserContext = createContext();

function App() {
  // this state will be shared with all components
  const [user, setUser] = useState();

  const [searchV, setSearchV] = useState("");

  const [mapAction, setMapAction] = useState(false);

  // const handleSearchApp = () => {
  //   setSearchTerm(searchTerm);
  // };

  const [visible, setVisible] = useState(false);
  const [radius, setRadius] = useState(10000);
  const [circleCenter, setCircleCenter] = useState({
    lat: 37.98381,
    lng: 23.727539,
  });
  const [selectedCategories, setSelectedCategories] = useState([])
  const [selectedKeywords, setSelectedKeywords] = useState([])

  let props = {
    visible: visible,
    setVisible: setVisible,
    radius: radius,
    setRadius: setRadius,
    circleCenter: circleCenter,
    setCircleCenter: setCircleCenter,
    searchV: searchV,
    setSearchV: setSearchV,
    mapAction : mapAction,
    setMapAction: setMapAction,
    selectedCategories: selectedCategories,
    setSelectedCategories: setSelectedCategories,
    selectedKeywords: selectedKeywords,
    setSelectedKeywords : setSelectedKeywords,
  };
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
          <Header {...props} />
          <Routes>
            <Route path="/" element={<HomeScreen {...props} />} />
            <Route path="/login/" element={<LoginScreen />} />
            <Route path="/register/" element={<RegisterScreen />} />
            <Route path="/admin_page/" element={<AdminsPage />} />
            <Route path="/save_searches/" element={<SaveSearches />} />
          </Routes>
        </Router>
      </UserContext.Provider>
    </div>
  );
}

export default App;
