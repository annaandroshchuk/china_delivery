from django.db import models
from solo.models import SingletonModel
from cloudinary.models import CloudinaryField


class SiteSettings(SingletonModel):
    """Singleton model for admin-editable site content."""

    # --- Header ---
    header_phone = models.CharField("Телефон у хедері", max_length=30, default="+38 067 611 96 22")
    header_cta_text = models.CharField("Текст кнопки хедеру", max_length=60, default="Отримати консультацію")

    # --- Hero ---
    hero_title = models.CharField("Заголовок hero", max_length=120, default="ДОСТАВКА ВАНТАЖУ З КИТАЮ")
    hero_subtitle = models.CharField(
        "Підзаголовок hero", max_length=120,
        default="7–10 днів • від $5,95/кг • з гарантією строків",
    )
    hero_description = models.TextField(
        "Опис hero",
        default=(
            "Знижуємо ваші логістичні витрати до 20% за рахунок прямої консолідації "
            "на власних складах у Китаї та оптимізації маршрутів без посередників."
        ),
    )
    hero_benefits = models.TextField(
        "Переваги під описом (кожна з нового рядка)",
        default="Без прихованих платежів.\nБез затримок.\nБез ризиків.",
    )
    hero_form_title = models.CharField(
        "Заголовок форми hero", max_length=120,
        default="Дізнайтесь, скільки можна зекономити на доставці з Китаю",
    )
    hero_form_subtitle = models.CharField(
        "Підзаголовок форми hero", max_length=160,
        default="Розрахуємо кращий тариф та оптимальну модель поставки",
    )

    # --- Stats ---
    stats_companies = models.CharField("Кількість компаній", max_length=20, default="5000")
    stats_years = models.CharField("Рік заснування", max_length=20, default="2009")

    # --- CTA banners ---
    cta_1_title = models.CharField(
        "CTA банер 1 — заголовок", max_length=160,
        default="Готові знизити витрати на доставку та уникнути ризиків?",
    )
    cta_1_text = models.TextField(
        "CTA банер 1 — текст",
        default=(
            "Залиште заявку — логістичний експерт прорахує оптимальний маршрут, "
            "покаже, де можна зекономити, та підбере формат доставки без прихованих платежів і затримок."
        ),
    )
    cta_2_title = models.CharField(
        "CTA банер 2 — заголовок", max_length=160,
        default="Дізнайтесь, скільки ви реально можете зекономити на доставці з Китаю",
    )
    cta_2_text = models.CharField(
        "CTA банер 2 — підзаголовок", max_length=200,
        default="Отримаєте персональний розрахунок та варіанти оптимізації маршруту з фіксованими строками",
    )

    # --- Contact form ---
    contact_form_title = models.CharField(
        "Заголовок форми контактів", max_length=120,
        default="Залишились запитання або хочете оформити замовлення?",
    )
    contact_form_subtitle = models.CharField(
        "Підзаголовок форми контактів", max_length=200,
        default="Заповніть форму та отримайте консультацію логістичного експерта",
    )

    # --- Footer ---
    footer_phone = models.CharField("Телефон у футері", max_length=30, default="+38 067 611 96 22")
    footer_email = models.EmailField("Email у футері", default="info@wingo.com.ua")
    footer_address = models.CharField("Адреса", max_length=200, default="Україна, Київ")
    footer_telegram = models.URLField("Telegram", blank=True, default="")
    footer_viber = models.URLField("Viber", blank=True, default="")
    footer_instagram = models.URLField("Instagram", blank=True, default="")
    footer_facebook = models.URLField("Facebook", blank=True, default="")
    footer_linkedin = models.URLField("LinkedIn", blank=True, default="")
    footer_copyright = models.CharField("Copyright", max_length=200, default="© 2009–2025 WINGO. Всі права захищені.")

    # --- Integrations ---
    gtm_container_id = models.CharField("GTM Container ID", max_length=20, blank=True, default="")
    bitrix_webhook_url = models.CharField(
        "Bitrix24 Webhook URL", max_length=500, blank=True, default="",
        help_text="https://your-domain.bitrix24.ua/rest/{user_id}/{webhook_code}",
    )
    ai_calculator_url = models.URLField(
        "URL AI-калькулятора", blank=True,
        default="https://wingo.com.ua/",
    )

    class Meta:
        verbose_name = "Налаштування сайту"

    def __str__(self) -> str:
        return "Налаштування сайту"


class LeadSubmission(models.Model):
    """Backup log of every form submission."""

    STATUS_PENDING = "pending"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "В обробці"),
        (STATUS_SENT, "Відправлено"),
        (STATUS_FAILED, "Помилка"),
    ]

    name = models.CharField("Ім'я", max_length=120)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email", blank=True, default="")
    form_location = models.CharField("Форма", max_length=60, default="hero")

    utm_source = models.CharField(max_length=200, blank=True, default="")
    utm_medium = models.CharField(max_length=200, blank=True, default="")
    utm_campaign = models.CharField(max_length=200, blank=True, default="")
    utm_content = models.CharField(max_length=200, blank=True, default="")
    utm_term = models.CharField(max_length=200, blank=True, default="")
    gclid = models.CharField("Google Click ID", max_length=200, blank=True, default="")
    fbclid = models.CharField("Facebook Click ID", max_length=200, blank=True, default="")

    bitrix_lead_id = models.CharField("ID ліда у Bitrix24", max_length=20, blank=True, default="")
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)

    ip_address = models.GenericIPAddressField("IP адреса", null=True, blank=True)
    user_agent = models.TextField("User-Agent", blank=True, default="")
    referrer = models.URLField("Referrer", blank=True, default="", max_length=500)
    page_url = models.URLField("URL сторінки", blank=True, default="", max_length=500)

    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} | {self.phone} | {self.created_at:%d.%m.%Y %H:%M}"


class FAQ(models.Model):
    """Frequently asked questions, admin-managed."""

    question = models.CharField("Питання", max_length=300)
    answer = models.TextField("Відповідь")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активне", default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["order"]

    def __str__(self) -> str:
        return self.question[:80]


class DeliveryCategory(models.Model):
    """Carousel item for 'What we deliver' section."""

    title = models.CharField("Назва", max_length=120)
    image = CloudinaryField("Зображення", folder="landing/categories/", blank=True, null=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Категорія товарів"
        verbose_name_plural = "Категорії товарів"
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title
