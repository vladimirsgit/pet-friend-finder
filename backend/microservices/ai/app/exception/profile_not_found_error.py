class ProfileNotFoundError(Exception):
    def __init__(self, message="Profile not found."):
        super().__init__(message)
        self.message = message