class AdoptionRequestNotFoundError(Exception):
    def __init__(self, message="Request not found."):
        super().__init__(message)
        self.message = message