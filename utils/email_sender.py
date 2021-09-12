import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def send_email(craigdata):

  content = table_maker(craigdata)
  send_message(content)

  return 1

def table_maker(craigdata):

  temp = Template('''
    <tr>
        <td>$num</td>
        <td><a href="$link">$title</a></td>
        <td>$town</td>
        <td>$price</td>
        <td>$distance</td>
        <td>$new</td>
    </tr>
  ''')

  table = ''
  counter = 1
  for item in craigdata:
    tr = temp.substitute(num=counter,link=item["link"], title=item["title"], town=item["town"],price=item["price"],distance=item["distance"],new= 'Yes' if item['isNew'] else '')
    table = table + tr
    counter = counter + 1

  return table

def send_message(content):
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
              font-family: arial, sans-serif\;
              border-collapse: collapse\;
            }
            
            td, th {
              border: 1px solid #dddddd\;
              text-align: left\;
              padding: 8px\;
            }
            
            tr:nth-child(even) {
              background-color: #dddddd\;
            }
            </style>
        </head>
        <body>
            <table style="width: max-content">
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Town</th>
              <th>Price</th>
              <th>Distance</th>
              <th>Is New</th>
            </tr>
              %s
            </table>

        </body>
    </html>
  """ % content 

  html = html.replace("\\",'')

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

  entry1 = {
    "title": 'Room in Franklin Lakes',
    "town": '(Franklin Lakes)',
    "link": 'https://wwww.google.com',
    "price": '$420',
    "distance": '5Mi'
  }

  entry2 = {
    "title": 'Room in Hoboken',
    "town": '(Hoboken)',
    "link": 'https://wwww.google.com',
    "price": '$420',
    "distance": '5Mi'
  }
  
  send_email([entry1,entry2])
  