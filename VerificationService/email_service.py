import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(to_email: str, verification_code: str):
    verification_link = f"http://localhost:8002/users/verify/{verification_code}"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email address"
    message["From"] = EMAIL_USERNAME
    message["To"] = to_email

    text = f"""
    Please verify your email address by clicking on the link below:
    {verification_link}
    
    If you did not request this verification, please ignore this email.
    """

    html = f"""
    <html>
        <body>
            <h2>Email Verification</h2>
            <p>Please verify your email address by clicking on the link below:</p>
            <p><a href="{verification_link}">Verify Email</a></p>
            <p>If you did not request this verification, please ignore this email.</p>
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
