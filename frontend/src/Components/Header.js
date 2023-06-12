import React, { useState } from 'react'
import "../App.js";
import "../Styles/Header.css";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';

function Header() {
  const [searchTerm, setSearchTerm, onSearch] = useState('');

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    onSearch(searchTerm);
  };
  return (
    <nav className="navbar">
      <div className="nav-left">
        <img style={{width:"20%", height:"20%"}} src="/geoxplorers_logo.png" alt="logo"/>
        <form className= "search-bar" onSubmit={handleFormSubmit}>
          <input
            className="search-input"
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={handleInputChange}
          />
          <button className="search-button" type="submit">Search</button>
        </form>
      </div>
      <ul className="navbar-nav">
        {/* <li className="nav-item" style={{width: "150px"}}>
          <a className="nav-link" href="#">Saved Searches</a>
        </li> */}

        {/* the items are going to change if the user is logged in or not */}
        <li className="nav-item">
          <a className="nav-link" href="#">Login</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="#">Register</a>
        </li>
      </ul>
    </nav>
  )
}

export default Header