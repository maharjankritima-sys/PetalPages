from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="journal_dashboard"),
    path("new/", views.create_journal, name="create_journal"),
]