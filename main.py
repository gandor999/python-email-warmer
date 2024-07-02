import asyncio

from classes.email.EmailWarmer import EmailWarmer

def main():
    email_warmer = EmailWarmer(asyncio)
    mockEmails = email_warmer.buildMockEmails().getMockEmails()

    for i in range(5):
        asyncio.run(email_warmer.executeWarmUp(mockEmails))


main()
