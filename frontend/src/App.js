import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import SignIn from "./components/SignIn";
import Products from "./components/Products";
import Search from "./components/Search";
import Root from "./components/Root";
import Home from "./components/Home";
import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Root />}>
          <Route path="home" element={<main><Home /></main>} />
          <Route path="signin" element={<main><SignIn /></main>} />
          <Route path="products" element={<main><Products /></main>} />
          <Route path="search" element={<main><Search /></main>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}


export default App;
