import React, { useState, useContext, useEffect } from 'react';
import "../Styles/Header.css";
import { Container, Form } from 'react-bootstrap';
import "../App.css";
import "../Styles/Login.css";
import axios from 'axios';
import { UserContext } from '../App';
import { useNavigate } from 'react-router-dom';

// // Create a new context for authentication
// const AuthContext = React.createContext();
// // Custom hook for using the authentication context
// const useAuth = () => useContext(AuthContext);

function LoginScreen() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, SetUser] = useContext(UserContext);
  const navigate = useNavigate();
  // useEffect(() => {
  //   if(user){
  //     //mavigate to home page
  //   }
  // }, [user]);

  // useEffect(() => {
  //   console.log(password)
  // }, [password]);

  //function that makes a call for login 
  const login = async(e) => {
    e.preventDefault();
    try {
      const config = {
        headers: {
          'Content-type': 'application/json'
        }
      }
      const { data } = await axios.post(
        'http://127.0.0.1:8000/api/login/',
        { 
          'username': username,
          'password': password  
        },
        config
      )

      SetUser(data)
      // put user in local storage
      localStorage.setItem("User", JSON.stringify(data));
      console.log(data);
      navigate('/');
      window.alert("Successful Log In!");
    } 
    catch (error) {
      window.alert("Wrong username or password. \nPlease, try again.")
    }
  }

  return (
    <div>
      <Container className="login-container">
        <form className="login" onSubmit={(e) => login(e)}>
          <h3>Sign In</h3>
          <div className="login-content">
            <label>Username:</label>
            <input 
              type="text" 
              placeholder="Enter Username" 
              onChange={(e)=> setUsername(e.target.value)}/>
            <br/>
            <label>Password:</label>
            <input 
              type="password" 
              placeholder="Enter Password"
              onChange={(e) => setPassword(e.target.value)}/>
            <button type='submit'>Login</button>
            <p className="bottom-text"><em><strong>Don't have an account?</strong> Register <a href="/register">here</a>.</em></p>
          </div>
        </form>
      </Container>
    </div>
  )
}

export default LoginScreen