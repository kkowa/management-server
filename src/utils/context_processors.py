from django.conf import settings
from django.http import HttpRequest


def settings_context(request: HttpRequest) -> dict:
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}
