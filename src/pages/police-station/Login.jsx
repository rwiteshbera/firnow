import React, { useState } from "react";
import "./Login.css";
import { Link } from "react-router-dom"
export default function Login() {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (event) => {
    const value = event.target.value;

    // Use a regular expression to check if the input contains only alphabets
    const onlyAlphabets = /^[A-Za-z]+$/;

    if (onlyAlphabets.test(value) || value === "") {
      // Update the state only if the input is valid (only alphabets) or empty
      setInputValue(value);
    }
  };

  return (
    <>
      <h2 className="form_title2">Log in</h2>
      <div className="add-container">
        <div className="details-container form_lodge2">
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
            <div className="submit_div" style={{width: '60%'}}>
               <button type="submit" className="submit_btn">
               Login
               </button>
            </div>
         
            </div>
            <Link to='/police-station/register'>
                 <u>Register here</u>
                 </Link>
        </div>
      </div>
      <div style={{padding: '40px'}}/>
    </>
  );
}
