class PetNotFoundError(Exception):
    def __init__(self, message="Pet not found."):
        super().__init__(message)
        self.message = message