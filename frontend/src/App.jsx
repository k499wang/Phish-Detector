import { useState } from 'react'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import { Routes, Route } from "react-router-dom";


function App() {

  return (
    <>
    <div className="flex flex-col h-screen">
      <NavBar />

      <div className="flex-grow mt-14">
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </div>

    </>

  )    
}

export default App
