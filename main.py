import asyncio
import smtplib, ssl
from typing import List
import dotenv
import os

from classes.email.EmailModel import EmailModel
from classes.email.EmailWarmer import EmailWarmer
from utils import read_json_file


def main():
    dotenv.load_dotenv()

    email_warmer = EmailWarmer(asyncio, smtplib, ssl, os)
    mock_emails = email_warmer.build_mock_emails().get_mock_emails()
    
    real_emails: List[EmailModel] = []
    json_emails = read_json_file("emails.json")

    for json_email in json_emails:
        real_emails.append(EmailModel(json_email["email"], json_email["password"]))

    # for i in range(5):
    asyncio.run(email_warmer.execute_warm_up(mock_emails))
    # asyncio.run(email_warmer.execute_warm_up(real_emails))


main()
