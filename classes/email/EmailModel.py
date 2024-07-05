class EmailModel:
    def __init__(self, emailAddress, password, isMock = False) -> None:
        self.__emailAddress = emailAddress
        self.__password = password
        self.__isMock = isMock
    pass

    def get_email_address(self):
        return self.__emailAddress
    
    def get_password(self):
        # TODO: put encryption around this part and put salt in
        return self.__password
    
    def isMock(self):
        return self.__isMock