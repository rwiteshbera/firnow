import React, { useState} from "react";
import './Login.css';


export default function Login(){

   
        const [inputValue, setInputValue] = useState('');
      
        const handleInputChange = (event) => {
          const value = event.target.value;
          
          // Use a regular expression to check if the input contains only alphabets
          const onlyAlphabets = /^[A-Za-z]+$/;
      
          if (onlyAlphabets.test(value) || value === '') {
            // Update the state only if the input is valid (only alphabets) or empty
            setInputValue(value);
          }
        };
      

    return(
       <>
          <div className="add-container">
                         

              <div className="details-container">

                   <div className="input-container">
                      <h5 className="input-header">Mail id</h5>
                      <input className="input" type="number" placeholder="Enter the mail id here"></input>
                   </div>


                   <div className="input-container">
                      <h5 className="input-header">Password</h5>
                      <input className="input" type="text"  value={inputValue}
                        placeholder="Enter the password here"></input>
                   </div>



                   <div className="input-container">
                      <h5 className="input-header">District</h5>
                      <input className="input" type="email" placeholder="Enter the district here"></input>
                   </div>
                    


                   <div className="input-container">
                      <h5 className="input-header">Name</h5>
                      <input className="input" type="text" placeholder="Enter the name of police station here"></input>
                   </div>

                   <div className="input-container">
                         <div className="save-btn">
                              <input type="button" value="LOG IN"></input>
                         </div>

                   </div>

              </div>
          </div>
       </>
    );
}



