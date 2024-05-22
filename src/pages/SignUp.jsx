import React, { useState } from "react";
import './Login.css';
import { TextField } from "@mui/material";
import axios from "axios";
import Autocomplete from "@mui/material/Autocomplete";


export default function SignUp() {


   const [inputValue, setInputValue] = useState('');

   return (
      <>
         <h2 className="form_title2">Sign Up</h2>
         <div className="form_lodge2">
            <div className="input-container">
               <h5 className="input-header">Police Station</h5>
               <TextField variant="outlined" className="form_text_3" type="text" placeholder="Enter police station"></TextField>
            </div>
            <div className="input-container">
               <h5 className="input-header">E-mail id</h5>
               <TextField variant="outlined" type="email" className="form_text_3" placeholder="Enter the mail id here"></TextField>
            </div>
            <div className="input-container">
               <h5 className="input-header">Create Password</h5>
               <TextField variant="outlined" className="form_text_3" type="password" placeholder="Create strong password"></TextField>
            </div>
            <div className="input-container">
               <h5 className="input-header">State</h5>
               <Autocomplete disablePortal id="combo-box-demo" options={state} className="selection_box"
                  renderInput={(params) => (
                     <TextField {...params} />
                  )}
               />
            </div>

            <div className="input-container">
               <h5 className="input-header">District</h5>
               <Autocomplete disablePortal id="combo-box-demo" options={state} className="selection_box"
                  renderInput={(params) => (
                     <TextField {...params} />
                  )}
               />
            </div>
            <div className="submit_div">
               <button type="submit" className="submit_btn">
                  Register
               </button>
            </div>

         </div>
      </>
   );
}

const state = [
   { label: "Andhra Pradesh" },
   { label: "Arunachal Pradesh" },
   { label: "Assam" },
   { label: "Bihar" },
   { label: "Chhattisgarh" },
   { label: "Goa" },
   { label: "Gujarat" },
   { label: "Haryana" },
   { label: "Himachal Pradesh" },
   { label: "Jharkhand" },
   { label: "Karnataka" },
   { label: "Kerala" },
   { label: "Madhya Pradesh" },
   { label: "Maharashtra" },
   { label: "Manipur" },
   { label: "Meghalaya" },
   { label: "Mizoram" },
   { label: "Nagaland" },
   { label: "Odisha" },
   { label: "Punjab" },
   { label: "Rajasthan" },
   { label: "Sikkim" },
   { label: "Tamil Nadu" },
   { label: "Telangana" },
   { label: "Tripura" },
   { label: "Uttar Pradesh" },
   { label: "Uttarakhand" },
   { label: "West Bengal" }
];




