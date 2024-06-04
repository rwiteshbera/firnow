otp_html = """\
<html>
  <head>
    <style>
      body {
        font-size: 16px;
      }
      span.otp {
        font-size: 2rem;
        background-color: gray;
        display: block;
        color: white;
        width: 13%;
        height: 3rem;
        text-align: center;
        margin: 1rem 4rem;
      }
      p {
        font-size: 1rem;
      }
      span.bold {
        font-weight: bold;
      }
    </style>
  </head>

  <body>
    <p>
      Your OTP for verifying your email is:
      <span class="otp bold">{otp}</span>
      This will going to expire in <span class="bold">5 minutes</span>.
    </p>

    <p>
      Sincerely,
      FIRNow Team
    </p>
  </body>
</html>
"""

otp_text = """
Your OTP for verifying your email is: 
{otp}
This will going to expire in 5 minutes.

Sincerely,
FIRNow Team
"""
