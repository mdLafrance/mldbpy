class IllegalKeyFunctionError(Exception):
    """Key attribute is not part of the schema."""


class IllegalEntryError(Exception):
    """Entry doesn't match the relation schema."""


class MissingAttributeError(Exception):
    """Attribute doesn't exist for relation."""


class DuplicateEntryError(Exception):
    """Entry already exists in relation."""


class AttributeDomainError(Exception):
    """Value is not legal in the domain of the attribute."""
