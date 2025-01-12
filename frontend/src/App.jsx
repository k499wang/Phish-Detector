import { useState } from 'react'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import About from './pages/About';
import { Routes, Route } from "react-router-dom";


function App() {

  return (
    <>
    <div className="flex flex-col h-screen">
      <NavBar />

      <div className="flex-grow mt-14">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </div>

    </>

  )    
}

export default App
