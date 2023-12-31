import React, { useState, useContext } from 'react';
import "../Styles/Header.css";
import { Container } from 'react-bootstrap';
import "../App.css";
import "../Styles/Login.css";
import axios from 'axios';
import { UserContext } from '../App';
import { useNavigate } from 'react-router-dom';
import { MdArrowBack } from 'react-icons/md';
import Loader from '../Components/Loader';


function RegisterScreen() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [mail, setMail] = useState('');
  const [user, SetUser] = useContext(UserContext);

  const [loading, setLoading] = useState(false)
  const navigate = useNavigate();
 
  /**
   * register function sends a POST request to a user registration API endpoint, saves the user data in 
   * local storage, and navigates to a specified page upon successful registration.
   * The parameter `e` is preventing the page from refreshing when the form is submitted.
   */
  const register = async(e) => {
    setLoading(true)
    e.preventDefault();
    try {
        const config = {
            headers: {
            'Content-type': 'application/json'
            }
        }
        const { data } = await axios.post(
            '/api/user/',
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
        setLoading(false)
        navigate('/');
    } 
    catch (error) {
        setLoading(false)
        window.alert(error)
    }
  }

  // handle the "Back" button
  const handleBack = () => {
    navigate(-1);
  }

  return (
    <div>

        <Loader isActive={loading}/>
        <Container className="login-container" style={{paddingBottom: "950px"}}>
        
        <button className="back-button" onClick={handleBack}>
          <MdArrowBack /> Back
        </button>

        {/* the className type is login because the css is similar to the login one */}
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
            <button type='submit'>Register</button>
            <p className="bottom-text"><em><strong>Already have an account?</strong> Sign In <a href="/login">here</a>.</em></p>
          </div>
        </form>
      </Container>
    </div>
  )
}

export default RegisterScreen