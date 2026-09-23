class DomainException(Exception):
    """
    Base exception class for all business domain errors.
    All specific domain exceptions must inherit from this class.
    """
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)

class EntityNotFoundException(DomainException):
    """Raised when a requested domain entity (Account, User, Transaction) is not found."""
    pass

class BusinessRuleException(DomainException):
    """Raised when a financial or domain business rule is violated (e.g., insufficient balance)."""
    pass

class ConflictException(DomainException):
    """Raised when a resource collision occurs (e.g., duplicate CPF or Email)."""
    pass

class UnauthorizedException(DomainException):
    """Raised when user authentication fails or credentials are invalid."""
    pass

class ForbiddenException(DomainException):
    """Raised when an authenticated user attempts to access a resource they do not own."""
    pass