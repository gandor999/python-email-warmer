import asyncio

# use coroutines instead of threads

# ["mockEmail0@something.com", "mockEmail1@something.com"]
def getMockEmails():
    mockEmails = []

    for i in range(101):
        mockEmails.append(f"mockEmail_{i}_@something.com")

    return mockEmails


async def mockSendingEmail(mockEmail, mockRecipient):
    print(f"{mockEmail} sending an email to {mockRecipient}")

    # TODO: make a real letter content
    # TODO: send to real emails
    # TODO: add function to login email
    # TODO: separate logics for email warmp up and logging in
    # TODO: in getting the emails from a json file put this login in a util dir

    await asyncio.sleep(2)
    print(f"{mockEmail} successfully sent an email to {mockRecipient}")


async def sendEmailsConcurrently(mockEmail, mockRecipients):
    async with asyncio.TaskGroup() as tg:
        for mockRecipient in mockRecipients:
            if mockEmail != mockRecipient:
                tg.create_task(mockSendingEmail(mockEmail, mockRecipient))


async def processEmailWarmUp():
    mockEmails = getMockEmails()

    async with asyncio.TaskGroup() as tg:
        # is this more readable than just directly doing sendEmailsConcurrently(mockEmail, mockEmails)?
        with mockEmails as mockRecipients:
            for mockEmail in mockEmails:
                tg.create_task(sendEmailsConcurrently(mockEmail, mockRecipients))

    print("Wait for 5 seconds")
    await asyncio.sleep(5)


def main():
    for i in range(5):
        asyncio.run(processEmailWarmUp())


main()
