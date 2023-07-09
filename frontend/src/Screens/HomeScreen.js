import React from "react";
import Map from "../Components/Map";
import Header from "../Components/Header";

function HomeScreen(props) {
  return (
    <div>
      <Map {...props} />
    </div>
  );
}

export default HomeScreen;
