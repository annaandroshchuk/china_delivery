"""
Bitrix24 CRM integration via outgoing webhook.

API: crm.lead.add
Docs: https://apidocs.bitrix24.com/api-reference/crm/leads/crm-lead-add.html

UTM fields are natively supported in Bitrix24 lead fields:
UTM_SOURCE, UTM_MEDIUM, UTM_CAMPAIGN, UTM_CONTENT, UTM_TERM
"""
from __future__ import annotations

import logging
from typing import Any

import requests
from django.conf import settings

logger = logging.getLogger("landing")

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 10


def create_bitrix_lead(data: dict[str, Any]) -> dict[str, Any]:
    """
    Send a lead to Bitrix24 CRM via webhook.

    Returns dict with keys:
        - success (bool)
        - lead_id (str | None) -- Bitrix24 lead ID on success
        - error (str | None)   -- error description on failure
    """
    webhook_url = getattr(settings, "BITRIX_WEBHOOK_URL", "").strip()

    if not webhook_url:
        logger.warning("BITRIX_WEBHOOK_URL is not configured — lead not sent to CRM")
        return {"success": False, "lead_id": None, "error": "Webhook URL not configured"}

    endpoint = webhook_url.rstrip("/") + "/crm.lead.add"

    name: str = data.get("name", "")
    phone: str = data.get("phone", "")
    email: str = data.get("email", "")
    form_location: str = data.get("form_location", "landing")
    page_url: str = data.get("page_url", "")

    utm_source: str = data.get("utm_source", "")
    utm_medium: str = data.get("utm_medium", "")
    utm_campaign: str = data.get("utm_campaign", "")
    utm_content: str = data.get("utm_content", "")
    utm_term: str = data.get("utm_term", "")
    gclid: str = data.get("gclid", "")
    fbclid: str = data.get("fbclid", "")
    referrer: str = data.get("referrer", "")

    comments_parts = [f"Форма: {form_location}", f"URL: {page_url}"]
    if gclid:
        comments_parts.append(f"gclid: {gclid}")
    if fbclid:
        comments_parts.append(f"fbclid: {fbclid}")
    if referrer:
        comments_parts.append(f"Referrer: {referrer}")
    comments = "\n".join(comments_parts)

    fields: dict[str, Any] = {
        "TITLE": f"Landing | {name} | {phone}",
        "NAME": name,
        "STATUS_ID": "NEW",
        "SOURCE_ID": "WEB",
        "SOURCE_DESCRIPTION": f"Лендінг — {form_location} | {page_url}",
        "OPENED": "Y",
        "COMMENTS": comments,
    }

    if phone:
        fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
    if email:
        fields["EMAIL"] = [{"VALUE": email, "VALUE_TYPE": "WORK"}]
    if utm_source:
        fields["UTM_SOURCE"] = utm_source
    if utm_medium:
        fields["UTM_MEDIUM"] = utm_medium
    if utm_campaign:
        fields["UTM_CAMPAIGN"] = utm_campaign
    if utm_content:
        fields["UTM_CONTENT"] = utm_content
    if utm_term:
        fields["UTM_TERM"] = utm_term

    payload = {
        "fields": fields,
        "params": {"REGISTER_SONET_EVENT": "Y"},
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        )
        response.raise_for_status()
        result = response.json()

        if "result" in result and result["result"]:
            lead_id = str(result["result"])
            logger.info("Bitrix24 lead created: ID=%s name=%s", lead_id, name)
            return {"success": True, "lead_id": lead_id, "error": None}

        error_msg = result.get("error_description", result.get("error", "Unknown Bitrix24 error"))
        logger.error("Bitrix24 API error: %s | payload=%s", error_msg, payload)
        return {"success": False, "lead_id": None, "error": error_msg}

    except requests.Timeout:
        logger.error("Bitrix24 request timed out for lead: %s", name)
        return {"success": False, "lead_id": None, "error": "Request timeout"}
    except requests.RequestException as exc:
        logger.error("Bitrix24 request failed: %s", exc)
        return {"success": False, "lead_id": None, "error": str(exc)}
