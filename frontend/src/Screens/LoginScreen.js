import React, { useState, useContext, useEffect } from 'react';
import "../Styles/Header.css";
import { Container, Form } from 'react-bootstrap';
import "../App.css";
import "../Styles/Login.css";
import axios from 'axios';
import { UserContext } from '../App';
import { useNavigate } from 'react-router-dom';
import { MdLogin, MdArrowBack } from 'react-icons/md'
import Loader from '../Components/Loader';

function LoginScreen() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, SetUser] = useContext(UserContext);

  const [loading, setLoading] = useState(false)
  const navigate = useNavigate();

  /**
  * The `login` function sends a POST request to a login API endpoint with the provided username and password, 
  * and stores the returned user data in local storage. The e is used to prevent the page from refreshing 
  * when the form is submitted.
  */
  const login = async(e) => {
    setLoading(true)
    e.preventDefault();
    try {
      const config = {
        headers: {
          'Content-type': 'application/json'
        }
      }
      const { data } = await axios.post(
        '/api/login/',
        { 
          'username': username,
          'password': password  
        },
        config
      )

      SetUser(data)
      // put user in local storage
      localStorage.setItem("User", JSON.stringify(data));

      setLoading(false)
      navigate('/');
      
    } 
    catch (error) {
      setLoading(false)
      console.log(error)
      window.alert("Wrong username or password. \nPlease, try again.")
    }
  }

  // handle the 'Back' button
  const handleBack = () => {
    navigate(-1);
  }

  return (
    <div>

      <Loader isActive={loading}/>

      <Container className="login-container">
          
        <button className="back-button" onClick={handleBack}>
          <MdArrowBack /> Back
        </button>
 
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
            
            <button type='submit'>
              <span style={{display: "inline-flex", alignItems: "center"}}>Login <MdLogin style={{marginTop: "2px"}}/></span>
            </button>
            
            <p className="bottom-text"><em><strong>Don't have an account?</strong> Register <a href="/register">here</a>.</em></p>
          </div>
        </form>
      </Container>
    </div>
  )
}

export default LoginScreen