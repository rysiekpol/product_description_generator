import React, { useState } from "react"
import {toast } from 'react-toastify';
import { useForm } from "react-hook-form"
import { useNavigate } from "react-router-dom";



function SignIn() {
  // Inside your component
  const navigate = useNavigate();
  let [authMode, setAuthMode] = useState("signin")
  let [showConfirmation, setShowConfirmation] = useState(false)
  const { register, handleSubmit, getValues, formState: { errors } } = useForm()

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  const handleConfirmation = (data, e) => {
    e.preventDefault()
    fetch('http://localhost:5001/user/confirm-email/' + e.target + "/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          key: data.confirmationToken,
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        setShowConfirmation(false)
      })
      .catch((error) => {
        console.error('Error:', error);
      }
      );
  }

  const handleSignIn = (data, e) => {
    e.preventDefault()
    fetch('http://localhost:5001/user/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        email: data.email,
        password: data.password,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.non_field_errors){
          toast.info(data.non_field_errors, {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            });
          }
        else {
          toast.success("Logged in successfully", {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            });
          navigate('/')
        }
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }


  const handleSignUp = (data, e) => {
    e.preventDefault()
    fetch('http://localhost:5001/user/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: data.email,
        password1: data.password,
        password2: data.password2,
      }),
    })
      .then(response => response.json())
      .then(data => {
        toast.info(String(data[0]), {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "colored",
          });
        console.log('Success:', data);
        setShowConfirmation(true)
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  if (showConfirmation) {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleSubmit(handleConfirmation)}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Confirm your account</h3>
            <div className="form-group mt-3">
              <label>Confirmation token</label>
              <input
                type="text"
                className="form-control mt-1"
                placeholder="Enter your confirmation token"
                {...register("confirmationToken", { required: true })}
              />
               {errors.confirmationToken && <p className="p-1 text-danger" >{errors.confirmationToken.message}</p>}
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Confirm
              </button>
            </div>
          </div>
        </form>
      </div>
    )
  }
  
  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleSubmit(handleSignIn)}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
                {...register("email", { required: "Email is required", pattern: { value: /^\S+@\S+$/i, message: "Invalid email address" }})}
              />
              {errors.email && <p className="p-1 text-danger" >{errors.email.message}</p>}
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
                {...register("password", { required: "Password is required", minLength: { value: 8, message: "Password must be at least 8 characters" }})}
              />
              {errors.password && <p className="p-1 text-danger" >{errors.password.message}</p>}
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
              Forgot <a href="/">password?</a>
            </p>
          </div>
        </form>
      </div>
    )
  }

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={handleSubmit(handleSignUp)}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign In</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
              {...register("email", { required: "Email is required", pattern: { value: /^\S+@\S+$/i, message: "Invalid email address" }})}
            />
            {errors.email && <p className="p-1 text-danger" >{errors.email.message}</p>}
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
              {...register("password", { required: "Password is required", minLength: { value: 8, message: "Password must be at least 8 characters" }})}
            />
            {errors.password && <p className="p-1 text-danger" >{errors.password.message}</p>}
          </div>
          <div className="form-group mt-3">
            <label>Repeat password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Repeat Password"
              {...register("password2", { required: "Repeat password is required", validate: (value) => value === getValues().password || "The passwords do not match" })}
            />
            {errors.password2 && <p className="p-1 text-danger">{errors.password2.message}</p>}
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
          <p className="text-center mt-2">
            Forgot <a href="/">password?</a>
          </p>
        </div>
      </form>
    </div>
  )
}

export default SignIn