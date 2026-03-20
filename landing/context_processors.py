from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


def site_settings(request: "HttpRequest") -> dict:
    """Inject SiteSettings singleton into every template context."""
    from .models import SiteSettings

    return {"site_settings": SiteSettings.get_solo()}
