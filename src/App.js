import {
  Routes,
  Route,
  } from "react-router-dom";

  import './App.css';
  import SideNav from './Components/SideNav';
  import AxisCamera from "./Pages/AxisCamera";
  import Home from "./Pages/Home";
  import NoTraffic from "./Pages/NoTraffic";
  import CobaltController from "./Pages/CobaltController";

function App() {
  return (
    <div className="App">
      <SideNav />

      <main>
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/axis" element={<AxisCamera />} />
          <Route path="/notraffic" element={<NoTraffic />}/>
          <Route path="/cobalt" element={<CobaltController />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
