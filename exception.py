

class StateMachineException(Exception):
    """
    Custom Exception raised by the State Machine when an error occurs
    """
    def __init__(self, message):
        super(StateMachineException, self).__init__(message)
        self.error = message
