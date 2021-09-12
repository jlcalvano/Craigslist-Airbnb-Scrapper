import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def table_maker():
  return



def send_email ():
  sender_email = config.sender_email
  receiver_email = config.receiver_email
  password = config.password

  message = MIMEMultipart("alternative")
  message["Subject"] = config.subject
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message
  html = """\
    <html>
        <head>
        <style>
            table {
              font-family: arial, sans-serif;
              border-collapse: collapse;
              width: 100%;
            }
            
            td, th {
              border: 1px solid #dddddd;
              text-align: left;
              padding: 8px;
            }
            
            tr:nth-child(even) {
              background-color: #dddddd;
            }
            </style>
        </head>
        <body>
            <h3> No New Listings Found</h3>

            <table style="width: max-content;">
                <tr>
                  <th>Name</th>
                  <th>Town</th>
                  <th>Price</th>
                  <th>Distance</th>
                </tr>
                <tr>
                  <td><a href="https://newjersey.craigslist.org/roo/d/wayne-private-room/7359826831.html">Private Room</a></td>
                  <td>(Pompton Lakes)</td>
                  <td>$150</td>
                  <td>2.9Mi</td>
                </tr>
              </table>

        </body>
    </html>
  """

  # Turn these into plain/html MIMEText objects
  body = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(body)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(config.username, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )


if __name__ == "__main__":
  send_email()