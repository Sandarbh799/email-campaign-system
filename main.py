import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import EMAIL, PASSWORD, SMTP_SERVER, PORT


from datetime import datetime
def log(status, email):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} | {status} | {email}\n")

def send_bulk():
    with open("emails.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            email = row["email"]

            print(f"Sending to {name}...")

            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = email
            msg["Subject"] = f"Hello {name}"

            html = f"""
            <html>
              <body style="font-family: Arial;">
                <h2>Hello {name},</h2>
                <p>This is my <b>Email Campaign</b>.</p>
              </body>
            </html>
            """

            msg.attach(MIMEText(html, "html"))

            for attempt in range(2):
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(EMAIL, PASSWORD)
                    server.send_message(msg)
                    server.quit()

                    print(f"Sent to {email}")
                    log("SUCCESS", email)
                    break

                except Exception as e:
                    if attempt == 1:
                        print(f"Failed to send to {email}")
                        log("FAILED", email)
                
send_bulk()