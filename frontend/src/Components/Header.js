import React, { useState, useEffect, useContext } from "react";
import "../App.js";
import "../Styles/Header.css";
import { LinkContainer } from "react-router-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Button from "react-bootstrap/Button";
import {
  Router,
  Routes,
  Route,
  useLocation,
  useNavigate,
} from "react-router-dom";
import LoginScreen from "../Screens/LoginScreen.js";
import { UserContext } from "../App.js";
import {
  MdManageAccounts,
  MdFilterAlt,
  MdOutlineWifiTethering,
  MdSearch,
  MdAccountCircle,
  MdLogin,
  MdPersonAdd,
  MdOutlineSaveAlt,
  MdLogout,
  MdSave,
  MdPerson,
} from "react-icons/md";
import NotBell from "../Components/NotBell.js";
import "../Styles/Not.css";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function Header(props) {
  const {
    visible,
    setVisible,
    radius,
    circleCenter,
    setMapAction,
    selectedCategories,
    selectedKeywords,
    savedSearchId,
  } = props;

  console.log(props);
  const [searchTerm, setSearchTerm] = useState("");

  const [user, SetUser] = useContext(UserContext);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const location = useLocation();

  const navigate = useNavigate();

  const handleButtonClick = () => {
    setMapAction(true);
  };

  const handleSearchClick = () => {
    props.setSearchV(searchTerm);
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
    //props.setSearchV(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    const cat = selectedCategories.toString();
    const keywords = selectedKeywords.toString();
    let lat = "";
    let lng = "";
    let km = "";
    if (visible) {
      lat = circleCenter.lat;
      lng = circleCenter.lng;
      km = radius;
    }
    navigate(
      `/?text=${searchTerm}&categories=${cat}&keywords=${keywords}&lat=${lat}&lng=${lng}&km=${km}`
    );
  };

  const handleSaveSearch = async () => {
    if (savedSearchId !== -1) {
      try {
        const config = {
          headers: {
            "Content-type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
        };
        const { data } = await axios.post(
          `http://localhost:8000/api/searches/?pk=${savedSearchId}`,
          {},
          config
        );
        toast("Search saved successfully!", { type: "success" });
      } catch (error) {
        console.error(error);
      }
    }
  };

  /*The logout function clears the user data and removes it from the local storage.*/
  const logout = () => {
    SetUser(undefined);
    localStorage.removeItem("User");
  };

  return (
    <div>
      <ToastContainer />
      <nav
        className={location.pathname === "/" ? "navbar-home" : "navbar-other"}
      >
        <div className="nav-left">
          <LinkContainer
            style={{ width: "80px", height: "80px", cursor: "pointer" }}
            to="/"
          >
            <img
              style={{ width: "20px", height: "20px" }}
              src="/geoxplorers_logo.png"
              alt="logo"
            />
          </LinkContainer>
          <form
            className="search-bar"
            style={{
              zIndex: location.pathname !== "/" && -999,
              opacity: location.pathname !== "/" && 0,
            }}
            onSubmit={handleFormSubmit}
          >
            <input
              className="search-input"
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={handleInputChange}
            />
            <button className="search-button" type="submit">
              <MdSearch /> Search
            </button>
          </form>
          <ul
            className="navbar-nav"
            style={{
              zIndex: location.pathname !== "/" && -999,
              opacity: location.pathname !== "/" && 0,
            }}
          >
            <li className="nav-item">
              <a
                className="nav-link"
                type="button"
                onClick={() => setVisible(!visible)}
              >
                <MdOutlineWifiTethering /> Radius
              </a>
            </li>
            <li className="nav-item" style={{ width: "90px" }}>
              <a className="nav-link" type="button" onClick={handleButtonClick}>
                <MdFilterAlt /> Filter
              </a>
            </li>
            {user ? (
              <li className="nav-item" style={{ width: "130px" }}>
                {/* <a className="nav-link" href="">
                <MdOutlineSaveAlt /> Save Search
              </a> */}
                <button
                  className="search-button"
                  type="button"
                  onClick={handleSaveSearch}
                >
                  <MdOutlineSaveAlt /> Save Search
                </button>
              </li>
            ) : null}
          </ul>
        </div>

        {/* the items are going to change depending on the user  (admin, logged in, etc.)*/}

        {user ? (
          <ul className="navbar-nav">
            <li className="nav-item" style={{ width: "50px" }}>
              <div className="magicbell-container">
                <NotBell />
              </div>
            </li>

            {user.is_staff && (
              <li className="nav-item" style={{ width: "135px" }}>
                <a className="nav-link" href="/admin_page/">
                  <MdManageAccounts /> Admin's Page
                </a>
              </li>
            )}
            <li
              className={`nav-item dropdown ${isDropdownOpen ? "show" : ""}`}
              style={{ width: "170px" }}
            >
              <a
                className="nav-link dropdown-toggle"
                href="#"
                role="button"
                onClick={toggleDropdown}
              >
                <MdPerson /> Account
              </a>
              <div className={`dropdown-menu ${isDropdownOpen ? "show" : ""}`}>
                <a className="dropdown-item" href="/save_searches/">
                  <MdSave /> Saved Searches
                </a>
                <a className="dropdown-item">
                  <MdAccountCircle /> Profile
                </a>
                <a className="dropdown-item" onClick={logout}>
                  <MdLogout /> Logout
                </a>
              </div>
            </li>
          </ul>
        ) : (
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/login/">
                <MdLogin /> Sign In
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/register/">
                <MdPersonAdd /> Register
              </a>
            </li>
          </ul>
        )}
      </nav>
    </div>
  );
}

export default Header;
