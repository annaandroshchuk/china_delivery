from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def gtm_head(container_id: str) -> str:
    """Render Google Tag Manager <script> for <head>."""
    if not container_id:
        return ""
    script = (
        "<!-- Google Tag Manager -->"
        "<script>"
        "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':"
        "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],"
        "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src="
        f"'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
        f"}})(window,document,'script','dataLayer','{container_id}');"
        "</script>"
        "<!-- End Google Tag Manager -->"
    )
    return mark_safe(script)


@register.simple_tag
def gtm_body(container_id: str) -> str:
    """Render Google Tag Manager <noscript> for <body>."""
    if not container_id:
        return ""
    noscript = (
        "<!-- Google Tag Manager (noscript) -->"
        f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={container_id}"'
        ' height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'
        "<!-- End Google Tag Manager (noscript) -->"
    )
    return mark_safe(noscript)


@register.filter
def splitlines(value: str) -> list[str]:
    """Split a string by newlines into a list."""
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def split_by_bullet(value: str) -> list[str]:
    """Split a string by bullet character (•) into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split('•') if item.strip()]


@register.filter
def split_title(value: str) -> list[str]:
    """Split title into two parts: before and after the last space before 'з'."""
    if not value:
        return ['', '']
    
    # Знаходимо останній пробіл перед словом, що починається з "з"
    parts = value.rsplit(' з ', 1)
    if len(parts) == 2:
        return [parts[0].strip(), 'з ' + parts[1].strip()]
    
    # Якщо не знайдено " з ", розбиваємо за останнім пробілом
    parts = value.rsplit(' ', 1)
    if len(parts) == 2:
        return [parts[0].strip(), parts[1].strip()]
    
    return [value, '']
