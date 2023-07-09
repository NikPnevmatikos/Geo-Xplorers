import React, { useState, useEffect, useContext  } from 'react'
import "../App.js";
import "../Styles/Header.css";
import { LinkContainer } from 'react-router-bootstrap'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
import { Router, Routes, Route, useLocation } from 'react-router-dom';
import LoginScreen from '../Screens/LoginScreen.js';
import { UserContext } from '../App.js';
import {  MdManageAccounts, MdFilterAlt, MdOutlineWifiTethering, MdSearch, 
          MdAccountCircle, MdLogin, MdPersonAdd, MdOutlineSaveAlt, MdLogout } from 'react-icons/md';

function Header() {
  const [searchTerm, setSearchTerm, onSearch] = useState('');
  const [user, SetUser] = useContext(UserContext);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    onSearch(searchTerm);
  };

  const logout = () => {
    SetUser(undefined);
    // put user in local storage
    localStorage.removeItem("User");
  }

  const location = useLocation();

  return (
    <div>
      <nav className={location.pathname === '/' ? 'navbar-home': 'navbar-other'}>
        <div className="nav-left">
          <LinkContainer style={{width:"80px", height:"80px", cursor : 'pointer'}} to="/">
            <img style={{width:"20px", height:"20px"}} src="/geoxplorers_logo.png" alt="logo"/>            
          </LinkContainer>
          {/* <div style={{zIndex: location.pathname !== '/' && 0}}> */}
            <form className= "search-bar" style={{zIndex: location.pathname !== '/' && -999, opacity: location.pathname !== '/' && 0 }} onSubmit={handleFormSubmit}>
              <input
                className="search-input"
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={handleInputChange}
              />
              <button className="search-button" type="submit">
                <MdSearch/> Search
              </button>
            </form>
            <ul className="navbar-nav" style={{zIndex: location.pathname !== '/' && -999, opacity: location.pathname !== '/' && 0 }}>
              <li className="nav-item">
                <a className="nav-link" href="">
                  <MdOutlineWifiTethering/> Radius
                </a>
              </li>
              <li className="nav-item" style={{width: "90px"}}>
                <a className="nav-link" href="">
                  <MdFilterAlt/> Filter
                </a>
              </li>
              <li className="nav-item" style={{width: "130px"}}>
                <a className="nav-link" href="">
                  <MdOutlineSaveAlt/> Save Search
                </a>
              </li>
            </ul>
          {/* </div> */}
          
        </div>
        

          {/* the items are going to change if the user is logged in or not */}
          
          {user ?
            <ul className="navbar-nav">
              {user.is_staff &&
                <li className="nav-item" style={{width: "135px"}}>
                  <a className="nav-link" href="/admin_page/">
                  <MdManageAccounts/> Admin's Page 
                  </a>
                </li>
              }
              
              <li className={`nav-item dropdown ${isDropdownOpen ? 'show' : ''}`} 
                  style={{width: "110px"}}>
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  onClick={toggleDropdown}
                >
                  Account
                </a>
                <div className={`dropdown-menu ${isDropdownOpen ? 'show' : ''}`}>
                  <a className="dropdown-item">
                    <MdAccountCircle/> Profile
                  </a>
                  <a className="dropdown-item" onClick={logout}>
                    <MdLogout/> Logout
                  </a>
                </div>
              </li>
            </ul>
          :
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link" href="/login/">
                  <MdLogin/> Sign In
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/register/">
                   <MdPersonAdd/> Register
                </a>
              </li>
            </ul>
          }
      </nav>
    </div>
  )
}

export default Header