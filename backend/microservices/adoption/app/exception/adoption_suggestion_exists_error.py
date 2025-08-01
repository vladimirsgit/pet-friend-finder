class AdoptionSuggestionExistsError(Exception):
    def __init__(self, message="Suggestion already exists."):
        super().__init__(message)
        self.message = message