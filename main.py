import asyncio
import smtplib, ssl
from typing import List
import dotenv
import os
import random
import logging

from classes.email.EmailModel import EmailModel
from classes.email.EmailWarmer import EmailWarmer
from utils import read_json_file


def main():
    dotenv.load_dotenv()
    logging.basicConfig(level=logging.INFO)

    email_warmer = EmailWarmer(asyncio, smtplib, ssl, os, logging)
    mock_emails = email_warmer.get_mock_emails(3)
    real_emails = email_warmer.get_real_emails("emails.json")

    # while True:
    # asyncio.run(email_warmer.execute_warm_up(mock_emails, 5))
    # asyncio.run(email_warmer.execute_warm_up(real_emails, random.randint(1800, 3600)))
    asyncio.run(email_warmer.execute_warm_up(real_emails, 5))


main()
