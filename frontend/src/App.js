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
          <Route index element={<Home />} />
          <Route path="signin" element={<SignIn />} />
          <Route path="products" element={<Products />} />
          <Route path="search" element={<Search />} />
        </Route>
      </Routes>
    </BrowserRouter>

  );
}


export default App;
