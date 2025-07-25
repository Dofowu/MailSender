from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

EMAIL = os.getenv("EMAIL")         # Your Gmail address
PASSWORD = os.getenv("PASSWORD")   # Your App Password

@app.route('/', methods=['POST'])
def send_email():
    to_email = request.form.get('to_email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not to_email or not subject or not message:
        return "Missing fields", 400

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        html_part = MIMEText(message, "html")
        msg.attach(html_part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, to_email, msg.as_string())

        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
