"""Локальний запуск: `manage.py` використовує `project.settings` → підключаємо develop.
У проді виставляйте DJANGO_SETTINGS_MODULE=project.settings.production."""

from .develop import *  # noqa: F401, F403
