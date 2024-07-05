import asyncio
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
import os

from classes.email.EmailModel import EmailModel


class EmailWarmer:

    def __init__(self, asyncio: asyncio, smtplib: smtplib, ssl: ssl, os: os) -> None:
        self.__mock_emails: List[EmailModel] = []
        self.__asyncio = asyncio
        self.__smtplib = smtplib
        self.__ssl = ssl
        self.__os = os
        # Would this benefit from creating a singleton LibraryManager for the libs being injected? It just seems to be more maintenance
        pass

    # [{"mockEmail0@something.com", "stub password"}, {"mockEmail1@something.com", "stub password"}]
    def build_mock_emails(self):
        for i in range(101):
            self.__mock_emails.append(
                EmailModel(
                    f"mockEmail_{i}_@something.com", "stub password", isMock=True
                )
            )

        return self

    def get_mock_emails(self):
        return self.__mock_emails

    async def send_email_message(
        self, sender_email: EmailModel, recipient_email: EmailModel
    ):
        if sender_email.isMock() and recipient_email.isMock():
            print(
                f"{sender_email.get_email_address()} sent a message to {recipient_email.get_email_address()}"
            )
            return

        port = self.__os.getenv("GOOGLE_SSL_PORT")
        sender_email_password = sender_email.get_password()
        sender_email = sender_email.get_email_address()
        recipient_email = recipient_email.get_email_address()

        plain_text = "Plain text | Warm up email"
        html_content = """\
            <html>
                <body>
                    <p>Warmup email</p>
                </body>
            </html>
        """

        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = "Warmup Email"

        part1 = MIMEText(plain_text, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)

        # Create a secure SSL context
        context = self.__ssl.create_default_context()

        with self.__smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, sender_email_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()

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

    async def execute_warm_up(self, emails: List[EmailModel]):
        tasks = []
        for sender_email in emails:
            tasks.append(self.send_emails_concurrently(sender_email, emails))
        await self.__asyncio.gather(*tasks)

        print("Wait for 5 seconds")
        await self.__asyncio.sleep(5)

        # await self.send_email_message("", "")
