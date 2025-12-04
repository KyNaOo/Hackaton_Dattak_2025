import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_email(target, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = target
    msg["Subject"] = subject

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, target, msg.as_string())
        print(f"[OK] Sent to {target}")

if __name__ == "__main__":
    with open("email_list.txt") as f:
        targets = [line.strip() for line in f if line.strip()]

    # phishing_subject = "⚠️ Important: Action Required for Your Account"
    # phishing_html = """
    # <h3>Security Verification Needed</h3>
    # <p>Your account requires verification. Please click the following link:</p>
    # <a href="https://example.com/verify">Verify Your Account</a>
    # <p>If you do not verify, your access may be limited.</p>
    # """
    phishing_subject = "Internal Update"
    phishing_html = """
    <p>Hello,</p>
    <p>This is an internal test message for our demo system.</p>
    """

    print(f"Sending {len(targets)} emails...")
    for t in targets:
        send_email(t, phishing_subject, phishing_html)
