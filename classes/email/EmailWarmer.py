import asyncio


class EmailWarmer:

    def __init__(self, asyncio: asyncio) -> None:
        self.__mockEmails = []
        self.__asyncio = asyncio
        pass

    # ["mockEmail0@something.com", "mockEmail1@something.com"]
    def buildMockEmails(self):
        for i in range(101):
            self.__mockEmails.append(f"mockEmail_{i}_@something.com")

        return self

    def getMockEmails(self):
        return self.__mockEmails

    async def mockSendingEmail(self, mockEmail, mockRecipient):
        print(f"{mockEmail} sending an email to {mockRecipient}")

        await asyncio.sleep(2)
        print(f"{mockEmail} successfully sent an email to {mockRecipient}")

    # use coroutines instead of threads
    async def sendEmailsConcurrently(self, mockEmail, mockRecipients):
        tasks = []
        for mockRecipient in mockRecipients:
            if mockEmail != mockRecipient:
                tasks.append(
                    self.__asyncio.create_task(
                        self.mockSendingEmail(mockEmail, mockRecipient)
                    )
                )
        await self.__asyncio.gather(*tasks)

    async def executeWarmUp(self, mockEmails):
        tasks = []
        for mockEmail in mockEmails:
            tasks.append(self.sendEmailsConcurrently(mockEmail, mockEmails))
        await self.__asyncio.gather(*tasks)

        print("Wait for 5 seconds")
        await self.__asyncio.sleep(5)
