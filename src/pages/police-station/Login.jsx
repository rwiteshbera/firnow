import React, { useState } from "react";
import "./Login.css";
import { Link } from "react-router-dom"
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = {
      username: email,
      password: password
    };

    try {
      const resp = await fetch(`http://127.0.0.1:8000/police-station/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(formData).toString()
      });

      if (resp.ok) {
        // If login is successful, get the access token from the response
        const data = await resp.json();
        const accessToken = data.accessToken;
        console.log(accessToken);
        // Store the access token in local storage or state for future use
        // Example: localStorage.setItem('accessToken', accessToken);

        // Redirect the user to the protected page
        window.location.href = 'src\pages\Dashboard.jsx';
      } else {
        // Handle error response
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  return (
    <>
      <h2 className="form_title2">Log in</h2>
      <div className="add-container">
        <div className="form_lodge2">
          <form onSubmit={handleLogin} >
            <div className="input-container">
              <h5 className="input-header">Mail id</h5>
              <input
                className="input"
                type="email"
                placeholder="Enter the mail id here"
              ></input>
            </div>

            <div className="input-container">
              <h5 className="input-header">Password</h5>
              <input
                className="input"
                type="password"
                placeholder="Enter the password here"
              ></input>
            </div>

            {/* <div className="input-container">
            <h5 className="input-header">District</h5>
            <input
              className="input"
              type=""
              placeholder="Enter the district here"
            ></input>
          </div>

          <div className="input-container">
            <h5 className="input-header">Name</h5>
            <input
              className="input"
              type="text"
              placeholder="Enter the name of police station here"
            ></input>
          </div> */}

            {/* <div className="input-container">
                         <div className="save-btn login_btn">
                              <input type="button" value="LOG IN"></input>
                         </div>

                   </div> */}
            <div className="input-container">
              <div className="submit_div" style={{ width: '60%' }}>
                <button type="submit" className="submit_btn">
                  Login
                </button>
              </div>

            </div>
          </form>
          <Link to='/police-station/register'>
            <u>Register here</u>
          </Link>
        </div>
      </div>
      <div style={{ padding: '40px' }} />
    </>
  );
}
