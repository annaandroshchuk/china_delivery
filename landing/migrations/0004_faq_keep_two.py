# Залишаємо лише два пункти FAQ з початкового набору

from django.db import migrations


_KEEP_ORDERED = (
    "Які реальні строки доставки з Китаю до України?",
    "Що входить у доставку «під ключ»?",
)


def prune_faq(apps, schema_editor):
    FAQ = apps.get_model("landing", "FAQ")
    keep = set(_KEEP_ORDERED)
    FAQ.objects.exclude(question__in=keep).delete()
    for order, question in enumerate(_KEEP_ORDERED):
        FAQ.objects.filter(question=question).update(order=order)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0003_seed_faq"),
    ]

    operations = [
        migrations.RunPython(prune_faq, noop_reverse),
    ]
