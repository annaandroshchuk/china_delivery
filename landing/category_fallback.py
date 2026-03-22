"""
Зображення для каруселі «З чим працюємо», коли в адмінці немає DeliveryCategory.

Безкоштовні аналоги за настроєм референсів (Unsplash / Pexels). iStock та Unsplash+ не використовуємо.
Unsplash: https://unsplash.com/license · Pexels: https://www.pexels.com/license/
"""

from __future__ import annotations

_Q = "auto=format&fit=crop&w=800&q=85"


def _u(photo: str) -> str:
    return f"https://images.unsplash.com/{photo}?{_Q}"


def _pexels(photo_id: int) -> str:
    return (
        f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg"
        f"?auto=compress&cs=tinysrgb&w=800"
    )


FALLBACK_CATEGORY_CARDS: list[dict[str, str]] = [
    {
        "title": "Обладнання для виробництв",
        "image": _u("photo-1684695747561-9372850cf165"),
        "alt": "Конвеєрна лінія та коробки на складі, логістика та виробництво",
    },
    {
        "title": "Батареї та сонячні станції",
        "image": "/static/landing/images/battery-solar-station-kit.png",
        "alt": "Портативна зарядна станція та складна сонячна панель на білому фоні",
    },
    {
        "title": "Обладнання для салонів краси",
        "image": "/static/landing/images/salon-beauty-equipment-blue.png",
        "alt": "Перукарські інструменти на білій стійці салону, розмитий інтер’єр дзеркал та підсвітки, холодна синьо-біла гама",
    },
    {
        "title": "Сільгосптехніка та обладнання",
        "image": "/static/landing/images/agri-machinery-showroom.png",
        "alt": "Сучасний ангар або шоурум: червоні трактори на відблисковій підлозі, білі стіни та освітлення",
    },
    {
        "title": "Косметика та beauty-гаджети",
        "image": "/static/landing/images/cosmetics-beauty-gadgets-set.png",
        "alt": "Подарунковий beauty-набір у рожевій коробці, косметика, губки для макіяжу, пелюстки троянд",
    },
    {
        "title": "Оптові поставки одягу та взуття",
        "image": "/static/landing/images/wholesale-clothing-rack.png",
        "alt": "Рейл з одягом на дерев’яних вішаках, перспектива вздовж ряду, розмитий фон",
    },
    {
        "title": "Авто- та мотозапчастини",
        "image": "/static/landing/images/auto-moto-parts-catalog.png",
        "alt": "Автозапчастини на білому фоні: шарніри, підшипник, помпа, кришка масла, кріплення",
    },
    {
        "title": "Зоотовари",
        "image": "/static/landing/images/zootovary-dog-kraft.png",
        "alt": "Собака біля крафт-пакетів корму та дерев’яної миски з сухим кормом на мармурі",
    },
    {
        "title": "Та багато іншого",
        "image": "/static/landing/images/logistics-box-taping.png",
        "alt": "Працівник на складі заклеює картонну коробку скотчем, стелажі на фоні",
    },
]
