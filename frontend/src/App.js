import './App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./Components/Home";
import SaveSearches from "./Components/SaveSearches";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="" element={<SaveSearches/>}/>
            </Routes>
        </Router>
    );
}

export default App;
