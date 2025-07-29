class InvalidAdoptionActionError(Exception):
    def __init__(self, message="Invalid action."):
        super().__init__(message)
        self.message = message