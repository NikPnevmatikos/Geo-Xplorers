import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./Components/Home";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/home" element={<Home/>}/>
            </Routes>
        </Router>
    );
}

export default App;
