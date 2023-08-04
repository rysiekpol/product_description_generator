import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import Products from "./components/Products";
import Search from "./components/Search";
import Root from "./components/Root";
import Home from "./components/Home";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Root />}>
          <Route index element={<Home />} />
          <Route path="signin" element={<SignIn />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="products" element={<Products />} />
          <Route path="search" element={<Search />} />
        </Route>
      </Routes>
    </BrowserRouter>

  );
}


export default App;
