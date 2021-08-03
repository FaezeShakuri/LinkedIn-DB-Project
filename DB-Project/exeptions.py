class LoginError(BaseException):
    pass

class SignupErrorEmail(BaseException):
    pass

class SignupErrorPassword(BaseException):
    pass

class InvitationErrorAlreadySent(BaseException):
    pass

class InvitationErrorAlreadyFollow(BaseException):
    pass

class InvitationErrorInvalidEmail(BaseException):
    pass

class ConversationAlreadyExists(BaseException):
    pass
