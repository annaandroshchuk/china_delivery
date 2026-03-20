from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path("", views.index, name="index"),
    path("submit-lead/", views.submit_lead, name="submit_lead"),
    path("healthz/", views.healthz, name="healthz"),
]
