from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from .models import DeliveryCategory, FAQ, LeadSubmission, SiteSettings

# ---- Admin site branding ----
admin.site.site_header = "Wingo — Адмін-панель"
admin.site.site_title  = "Wingo CMS"
admin.site.index_title = "Управління сайтом"


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ("🔵 Хедер", {
            "fields": ("header_phone", "header_cta_text"),
        }),
        ("🏠 Hero-секція", {
            "fields": (
                "hero_title",
                "hero_subtitle",
                "hero_description",
                "hero_benefits",
                "hero_form_title",
                "hero_form_subtitle",
            ),
        }),
        ("📊 Статистика", {
            "fields": ("stats_companies", "stats_years"),
        }),
        ("📣 CTA банери", {
            "fields": (
                "cta_1_title",
                "cta_1_text",
                "cta_2_title",
                "cta_2_text",
            ),
        }),
        ("📬 Контактна форма", {
            "fields": ("contact_form_title", "contact_form_subtitle"),
        }),
        ("🔗 Футер", {
            "fields": (
                "footer_phone",
                "footer_email",
                "footer_address",
                "footer_telegram",
                "footer_viber",
                "footer_instagram",
                "footer_facebook",
                "footer_linkedin",
                "footer_copyright",
            ),
        }),
        ("⚙️ Інтеграції", {
            "fields": (
                "gtm_container_id",
                "bitrix_webhook_url",
                "ai_calculator_url",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(LeadSubmission)
class LeadSubmissionAdmin(admin.ModelAdmin):
    list_display  = ("name", "phone", "email", "form_location", "status", "utm_source", "utm_campaign", "bitrix_lead_id", "created_at")
    list_filter   = ("status", "form_location", "created_at")
    search_fields = ("name", "phone", "email", "utm_source", "utm_campaign", "bitrix_lead_id")
    readonly_fields = (
        "name", "phone", "email", "form_location",
        "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
        "gclid", "fbclid", "bitrix_lead_id",
        "ip_address", "user_agent", "referrer", "page_url", "created_at",
    )
    fieldsets = (
        ("Контактні дані", {
            "fields": ("name", "phone", "email", "form_location", "status", "bitrix_lead_id"),
        }),
        ("UTM / Джерело", {
            "fields": ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "fbclid"),
        }),
        ("Технічна інформація", {
            "fields": ("ip_address", "user_agent", "referrer", "page_url", "created_at"),
        }),
    )

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display       = ("question_short", "order", "is_active")
    list_editable      = ("order", "is_active")
    list_display_links = ("question_short",)
    ordering           = ("order",)

    def question_short(self, obj: FAQ) -> str:
        return obj.question[:80]
    question_short.short_description = "Питання"


@admin.register(DeliveryCategory)
class DeliveryCategoryAdmin(admin.ModelAdmin):
    list_display       = ("title", "image_preview", "order", "is_active")
    list_editable      = ("order", "is_active")
    list_display_links = ("title",)
    ordering           = ("order",)

    def image_preview(self, obj: DeliveryCategory) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:6px;object-fit:cover;">',
                obj.image.url,
            )
        return "—"
    image_preview.short_description = "Фото"
