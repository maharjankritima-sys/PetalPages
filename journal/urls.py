from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="journal_dashboard"),
    path("new/", views.create_journal, name="create_journal"),
     path("<int:journal_id>/", views.journal_detail, name="journal_detail"),
     path(
    "<int:journal_id>/edit/",
    views.edit_journal,
    name="edit_journal",
),
path(
    "<int:journal_id>/delete/",
    views.delete_journal,
    name="delete_journal",
),
path("trash/", views.trash, name="trash"),
path(
    "<int:journal_id>/delete-permanently/",
    views.delete_permanently,
    name="delete_permanently",
),
path("favorite/<int:journal_id>/", views.toggle_favorite, name="toggle_favorite"),
path(
    "restore/<int:journal_id>/",
    views.restore_journal,
    name="restore_journal"
),
path("profile/", views.profile, name="profile"),
]
