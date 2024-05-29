import React, { useState } from "react";
import './Login.css';

const VerifyEmail = () => {
    const [otp, setOtp] = useState('');

    const handleVerifyEmail = async () => {
        const formData = { otp: otp };

        try {
            const resp = await fetch(
                `http://127.0.0.1:8000/police-station/verify-email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${localStorage.getItem('accessToken')}` // storing the access token in localStorage
                    },
                    body: JSON.stringify(formData)
                }
            );

            const data = await resp.json();
            console.log(data);
        } catch (error) {
            console.error('Error verifying email:', error);
        }
    };

    return (
        <div className="add-container">
            <div className="details-container form_lodge2">
                <h2 className="form_title2">Verify Email</h2>
                <div className="input-container">
                    <h5 className="input-header">OTP</h5>
                    <input
                        type="text"
                        className="input form_text_3"
                        placeholder="Enter OTP"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                    />
                </div>
                <div className="submit_div">
                    <button type="button" className="submit_btn" onClick={handleVerifyEmail}>
                        Verify Email
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VerifyEmail;
