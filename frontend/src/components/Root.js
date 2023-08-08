import React, { useEffect } from 'react';
import Navbar from "./Navbar";
import Footer from './Footer';
import { Outlet, useNavigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import {toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Root() {
  const navigate = useNavigate();

  useEffect(() => {
    const checkTokenValidity = async () => {
      const token = localStorage.getItem('access_token');

      if (!token) {
        navigate('/signin');
        return;
      }

      try {
        const response = await fetch('http://localhost:5001/user/token/verify/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            token: localStorage.getItem('access_token'),
          }),

        });

        if (response.status === 401) {
          const refreshResponse = await fetch('http://localhost:5001/user/token/refresh/', {
            method: 'POST',
            credentials: 'include'
          });

          if (refreshResponse.ok) {
            // If refresh succeeded, save the new token and continue
            const data = await refreshResponse.json();
            localStorage.setItem('access_token', data.access_token);
          } else {
            // If refresh also failed, redirect to signup
            toast.error('Your session has expired. Please sign in again.', {
              position: "top-center",
              autoClose: 3000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: false,
              draggable: true,
              progress: undefined,
              theme: "colored",
            });
            navigate('/signin');
          }
        }
      } catch (error) {
        console.error('Error verifying token:', error);
      }
    };

    checkTokenValidity();
  }, [navigate]);

  return (
    <>
      <ToastContainer />
      <Navbar />
      <Outlet />
      <Footer />
    </>
  );
}

export default Root;
