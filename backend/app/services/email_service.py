import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_alert_email(subject, message):

    smtp_server = os.getenv(
        "SMTP_SERVER"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            587
        )
    )

    smtp_email = os.getenv(
        "SMTP_EMAIL"
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )

    alert_receiver = os.getenv(
        "ALERT_RECEIVER"
    )

    if (
        not smtp_email or
        not smtp_password or
        not alert_receiver
    ):

        print(
            "SMTP no configurado",
            flush=True
        )

        return

    email = MIMEMultipart()

    email["From"] = smtp_email
    email["To"] = alert_receiver
    email["Subject"] = subject

    email.attach(
        MIMEText(
            message,
            "plain"
        )
    )

    server = smtplib.SMTP(
        smtp_server,
        smtp_port
    )

    server.starttls()

    server.login(
        smtp_email,
        smtp_password
    )

    server.send_message(
        email
    )

    server.quit()

    print(
        "Correo enviado correctamente",
        flush=True
    )