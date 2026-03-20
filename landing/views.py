from __future__ import annotations

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import LeadForm
from .models import DeliveryCategory, FAQ, LeadSubmission
from .services.bitrix import create_bitrix_lead
from .utils import get_client_ip

logger = logging.getLogger("landing")


def index(request: HttpRequest) -> HttpResponse:
    """Main landing page."""
    faqs = FAQ.objects.filter(is_active=True)
    categories = DeliveryCategory.objects.filter(is_active=True)
    hero_form = LeadForm(initial={"form_location": "hero"})
    contact_form = LeadForm(initial={"form_location": "contact"})
    popup_form = LeadForm(initial={"form_location": "popup"})

    context = {
        "faqs": faqs,
        "categories": categories,
        "hero_form": hero_form,
        "contact_form": contact_form,
        "popup_form": popup_form,
    }
    return render(request, "landing/index.html", context)


@require_POST
def submit_lead(request: HttpRequest) -> HttpResponse:
    """
    HTMX endpoint: validate form, save to DB, push to Bitrix24.
    Returns partial HTML (success message or form with errors).
    """
    form = LeadForm(request.POST)

    if not form.is_valid():
        form_location = request.POST.get("form_location", "hero")
        return render(
            request,
            "landing/components/lead_form_partial.html",
            {"form": form, "form_location": form_location},
            status=422,
        )

    data = form.cleaned_data
    form_location: str = data.get("form_location", "hero")

    submission = LeadSubmission(
        name=data["name"],
        phone=data["phone"],
        email=data.get("email", ""),
        form_location=form_location,
        utm_source=data.get("utm_source", ""),
        utm_medium=data.get("utm_medium", ""),
        utm_campaign=data.get("utm_campaign", ""),
        utm_content=data.get("utm_content", ""),
        utm_term=data.get("utm_term", ""),
        gclid=data.get("gclid", ""),
        fbclid=data.get("fbclid", ""),
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        referrer=request.META.get("HTTP_REFERER", "")[:500],
        page_url=request.POST.get("page_url", "")[:500],
        status=LeadSubmission.STATUS_PENDING,
    )
    submission.save()

    bitrix_data = {
        "name": data["name"],
        "phone": data["phone"],
        "email": data.get("email", ""),
        "form_location": form_location,
        "utm_source": data.get("utm_source", ""),
        "utm_medium": data.get("utm_medium", ""),
        "utm_campaign": data.get("utm_campaign", ""),
        "utm_content": data.get("utm_content", ""),
        "utm_term": data.get("utm_term", ""),
        "gclid": data.get("gclid", ""),
        "fbclid": data.get("fbclid", ""),
        "referrer": request.META.get("HTTP_REFERER", ""),
        "page_url": request.POST.get("page_url", ""),
    }

    result = create_bitrix_lead(bitrix_data)

    if result["success"]:
        submission.bitrix_lead_id = result["lead_id"]
        submission.status = LeadSubmission.STATUS_SENT
    else:
        submission.status = LeadSubmission.STATUS_FAILED
        logger.error(
            "Lead saved to DB (id=%d) but Bitrix24 failed: %s",
            submission.pk,
            result["error"],
        )

    submission.save(update_fields=["bitrix_lead_id", "status"])

    return render(
        request,
        "landing/components/success_message.html",
        {"form_location": form_location},
    )


def healthz(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", content_type="text/plain")
