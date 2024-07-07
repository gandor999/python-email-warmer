import asyncio
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
import os

from classes.email.EmailModel import EmailModel
from utils import read_file


class EmailWarmer:

    def __init__(self, asyncio: asyncio, smtplib: smtplib, ssl: ssl, os: os) -> None:
        self.__asyncio = asyncio
        self.__smtplib = smtplib
        self.__ssl = ssl
        self.__os = os
        # Would this benefit from creating a singleton LibraryManager for the libs being injected? It just seems to be more maintenance
        pass

    # [{"mockEmail0@something.com", "stub password"}, {"mockEmail1@something.com", "stub password"}]
    def get_mock_emails(self, number_of_emails: int = 101):
        mock_emails: List[EmailModel] = []
        for i in range(number_of_emails):
            mock_emails.append(
                EmailModel(
                    f"mockEmail_{i}_@something.com", "stub password", isMock=True
                )
            )
        return mock_emails

    def get_real_emails(self, json_filename: str):
        real_emails: List[EmailModel] = []
        json_emails: list[dict] = read_json_file(json_filename)

        for json_email in json_emails:
            real_emails.append(EmailModel(json_email["email"], json_email["password"]))

        return real_emails

    async def send_email_message(
        self, sender_email: EmailModel, recipient_email: EmailModel
    ):
        if sender_email.isMock() and recipient_email.isMock():
            print(
                f"{sender_email.get_email_address()} sending message to {recipient_email.get_email_address()}"
            )

            await asyncio.sleep(2)

            print(
                f"{sender_email.get_email_address()} sent a message to {recipient_email.get_email_address()}"
            )
            return

        port = self.__os.getenv("GOOGLE_SSL_PORT")
        sender_email_password = sender_email.get_password()
        sender_email = sender_email.get_email_address()
        recipient_email = recipient_email.get_email_address()

        html_content = read_file("content.html")

        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = "Warmup Email"

        body = MIMEText(html_content, "html")

        msg.attach(body)

        context = self.__ssl.create_default_context()

        try:
            with self.__smtplib.SMTP_SSL(
                "smtp.gmail.com", port, context=context
            ) as server:
                server.login(sender_email, sender_email_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                self.__logger.info(
                    f"{self.__log_tag} | send_email_message() | {sender_email} successfully sent a message to {recipient_email}"
                )
                server.quit()
        except Exception as e:
            self.__logger.warning(
                f"{self.__log_tag} | send_email_message() | sender_email: {sender_email} | recipient_email: {recipient_email} | exception | {e}"
            )

    # use coroutines instead of threads
    async def send_emails_concurrently(
        self, sender_email: EmailModel, recipient_emails: List[EmailModel]
    ):
        tasks = []
        for recipientEmail in recipient_emails:
            if sender_email.get_email_address() != recipientEmail.get_email_address():
                tasks.append(
                    self.__asyncio.create_task(
                        self.send_email_message(sender_email, recipientEmail)
                    )
                )
        await self.__asyncio.gather(*tasks)

    async def execute_warm_up(
        self, emails: List[EmailModel], interval_time: int = 1800
    ):
        tasks = []
        for sender_email in emails:
            tasks.append(self.send_emails_concurrently(sender_email, emails))
        await self.__asyncio.gather(*tasks)

        print(f"Wait for {interval_time} seconds")
        await self.__asyncio.sleep(interval_time)
