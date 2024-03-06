"""Custom exceptions."""


class AllegroError(Exception):
    """General Exception for this app."""


class AllegroConnectionError(AllegroError):
    """Unexpected connection state."""
