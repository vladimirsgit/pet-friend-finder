class AdoptionRequestExistsError(Exception):
    def __init__(self, message="Request already exists."):
        super().__init__(message)
        self.message = message