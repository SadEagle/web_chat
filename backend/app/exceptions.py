class DuplicateError(Exception):
    """Unique constraint disables insertion of the row"""


class NoCreatedElementError(Exception):
    """None rows was created in database error"""
