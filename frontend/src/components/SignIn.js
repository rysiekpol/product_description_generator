import React, { useState } from "react"
import {toast } from 'react-toastify';
import { useForm } from "react-hook-form"
import { useNavigate } from "react-router-dom";
import "./SignInStyles.css"


function SignIn() {
  // Inside your component
  const navigate = useNavigate();
  let [authMode, setAuthMode] = useState("signin")
  let [showConfirmation, setShowConfirmation] = useState(false)
  let [showResetPassword, setShowResetPassword] = useState(false)
  const { register, handleSubmit, getValues, formState: { errors } } = useForm()

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  const changeResetState = () => {
    setShowResetPassword(!showResetPassword)
  }

  const handleConfirmation = (data, e) => {
    e.preventDefault()
    fetch('http://localhost:5001/user/confirm-email/' + data.confirmationToken + "/", {
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
        toast.info("You may now login", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "colored",
        });
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
          localStorage.setItem('access_token', data.access)
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
        toast.info(data.detail, {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "colored",
          });
        if (data.detail === "Verification e-mail sent.") {
          toast.info("Please check your email for the confirmation token", {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            });
          setShowConfirmation(true)
        }
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const handleResetPassword = (data, e) => {
    e.preventDefault()
    fetch('http://localhost:5001/user/password/reset/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: data.email,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail === "Password reset e-mail has been sent.") {
          toast.info("Please check your email for the password reset token", {
            position: "top-center",
            autoClose: 3000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            });
          setShowResetPassword(false)
        }
        console.log('Success:', data);
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

  if (showResetPassword) {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleSubmit(handleResetPassword)}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Reset your password</h3>
            <div className="text-center">
              Got lost?{" "}
              <span className="link-primary" onClick={changeResetState}>
                Go Back
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter your email address"
                {...register("email", { required: true })}
              />
                {errors.email && <p className="p-1 text-danger" >{errors.email.message}</p>}
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Reset
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
            <button href="#" className="link-primary link-button" onClick={(e) => setShowResetPassword(true)}>Forgot password?</button>
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
          <button href="#" className="link-primary link-button" onClick={(e) => setShowResetPassword(true)}>Forgot password?</button>
          </p>
        </div>
      </form>
    </div>
  )
}

export default SignIn