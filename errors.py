class IncorrectDataRecievedError(Exception):
    def __str__(self):
        return 'Incorrect message from remote computer was received.'


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    def __str__(self):
        return 'Function argument must be a dictionary.'


class ReqFieldMissingError(Exception):
    def __init__(self, missingField):
        self.missingField = missingField

    def __str__(self):
        return f'There is no required field in received dictionary: {self.missingField}.'
