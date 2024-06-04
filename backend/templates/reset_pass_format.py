reset_pass_html = """\
<html>
  <head>
    <style>
      body {
        font-size: 16px;
      }

      span.bold {
        font-weight: bold;
      }

      p, a {
        font-size: 1rem;
        font-weight: normal;
      }
    </style>
  </head>

  <body>
    <p>
      Greetings {name},
    </p>

    <p>
      We received a request to reset your password for your account. If you did not make this 
      request, please ignore this email. Otherwise, please click the link below to create a new 
      password:
    </p>

    <p>
      <a href='{reset_pass_url}'>
        Reset Password
      </a>
    </p>

    <p>
      This link will expire in <span class='bold'>24 hours</span>, so be sure to use it right 
      away.
    </p>

    <p>
      If you have any questions or need further assistance, please contact our support team.
    </p>

    <p>
      Thank you for using our service!
    </p>

    <p>
      Sincerely, <br>
      FIRNow Team
    </p>
  </body>
</html>
"""

reset_pass_text = """\
Greetings {name},

We received a request to reset your password for your account. If you did not make this request, please ignore this email. Otherwise, please click the link below to create a new password:

{reset_pass_url}

This link will expire in 24 hours, so be sure to use it right away.

If you have any questions or need further assistance, please contact our support team.

Thank you for using our service!

Sincerely, 
FIRNow Team
"""
