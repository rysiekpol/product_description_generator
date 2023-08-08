import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import Logo from '../main_logo.svg';
import "./NavbarStyles.css";

class Navbar extends Component {
  state = { clicked: false };

  handleClick = () => {
    this.setState({ clicked: !this.state.clicked });
  };

  render() {
    return (
      <>
        <nav id="mainNav">
          <img src={Logo} alt="SVG" style={{ borderRadius: '50%' }} />

          <div>
            <ul
              id="navbar"
              className={this.state.clicked ? "#navbar active" : "#navbar"}
            >
              <li>
                <NavLink to="/home">
                  Home
                </NavLink>
              </li>
              <li>
                <NavLink to="/signin">Sign In</NavLink>
              </li>
              <li>
                <NavLink to="/products">Products</NavLink>
              </li>
              <li>
                <NavLink to="/search">Search</NavLink>
              </li>
            </ul>
          </div>

          <div id="mobile" onClick={this.handleClick}>
            <i
              id="bar"
              className={this.state.clicked ? "fas fa-times" : "fas fa-bars"}
            ></i>
          </div>
        </nav>
      </>
    );
  }
}

export default Navbar;