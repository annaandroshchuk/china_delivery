from __future__ import annotations

from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str | None:
    """Extract real client IP from request, respecting proxy headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def extract_utm_from_request(request: HttpRequest) -> dict[str, str]:
    """
    Extract UTM parameters from GET params or cookies.
    GET params take priority over cookies.
    """
    utm_keys = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "fbclid"]
    result: dict[str, str] = {}
    for key in utm_keys:
        value = request.GET.get(key) or request.COOKIES.get(key, "")
        result[key] = value[:200]
    return result
