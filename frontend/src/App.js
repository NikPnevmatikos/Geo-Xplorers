import './App.css';
import './bootstrap.min.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./Components/Home";
import Header from './Components/Header';


function App() {
    return (
        <div>
            <Header/>
                            
            {/* <img
                src="https://imageio.forbes.com/blogs-images/cognitiveworld/files/2019/06/types-of-AI.jpg?format=jpg&width=960"
                style={{ width: "100%", height: "100vh"}}
                alt="First slide"
            />                 */}
            <Router>
                <Routes>
                    <Route path="" element={<Home/>}/>
                </Routes>
            </Router>    
        </div>
        
    );
}

export default App;
