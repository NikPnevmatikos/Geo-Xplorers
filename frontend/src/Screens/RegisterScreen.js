import React, { useState, useContext, useEffect } from 'react';
import "../Styles/Header.css";
import { Container, Form } from 'react-bootstrap';
import "../App.css";
import "../Styles/Login.css";
import axios from 'axios';
import { UserContext } from '../App';
import { useNavigate } from 'react-router-dom';
import { MdArrowBack } from 'react-icons/md';
// // Create a new context for authentication
// const AuthContext = React.createContext();

// // Custom hook for using the authentication context
// const useAuth = () => useContext(AuthContext);

function RegisterScreen() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [mail, setMail] = useState('');
  const [user, SetUser] = useContext(UserContext);
  const navigate = useNavigate();

  // useEffect(() => {
  //   console.log(username)
  // }, [username]);

  // useEffect(() => {
  //   console.log(password)
  // }, [password]);

  //function that makes a call for login 
  const register = async(e) => {
    e.preventDefault();
    try {
        const config = {
            headers: {
            'Content-type': 'application/json'
            }
        }
        const { data } = await axios.post(
            'http://127.0.0.1:8000/api/user/',
            { 
            'username': username,
            'password': password,
            "email": mail,
            "first_name": firstName,
            "last_name": lastName 
            },
            config
        )

        SetUser(data)

        // put user in local storage
        localStorage.setItem("User", JSON.stringify(data));
        console.log(data);
        navigate('/');
        window.alert("Successful Registration!");
    } 
    catch (error) {
        window.alert(error)
    }
  }

  const handleBack = () => {
    navigate(-1);
  }

  return (
    <div>
        <Container className="login-container" style={{paddingBottom: "950px"}}>
          
        <button className="back-button" onClick={handleBack}>
          <MdArrowBack /> Back
        </button>
        {/* the className type is login because it's similar to the login one */}
        <form className="login" 
            style={{top: "500px"}}
            onSubmit={(e) => register(e)}>
          <h3>Register</h3>
          <div className="login-content">
            <label>Username:</label>
            <input 
              type="text" 
              placeholder="Enter Username" 
              onChange={(e)=> setUsername(e.target.value)}/>
            <br/>
            <label>First Name:</label>
            <input 
              type="text" 
              placeholder="Enter First Name" 
              onChange={(e)=> setFirstName(e.target.value)}/>
            <br/>
            <label>Last Name:</label>
            <input 
              type="text" 
              placeholder="Enter Last Name" 
              onChange={(e)=> setLastName(e.target.value)}/>
            <br/>
            <label>Email:</label>
            <input 
              type="text" 
              placeholder="Enter Email" 
              onChange={(e)=> setMail(e.target.value)}/>
            <br/>
            <label>Password:</label>
            <input 
              type="password" 
              placeholder="Enter Password"
              onChange={(e) => setPassword(e.target.value)}/>
            <br/>
            {/* <br/>
            <label>Confirm Password:</label>
            <input 
              type="password" 
              placeholder="Enter Password"
              onChange={(e) => setPassword(e.target.value)}/> */}
            <button type='submit'>Register</button>
            <p className="bottom-text"><em><strong>Already have an account?</strong> Sign In <a href="/login">here</a>.</em></p>
          </div>
        </form>
      </Container>
    </div>
  )
}

export default RegisterScreen