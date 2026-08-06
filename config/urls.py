from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from accounts.forms import LoginForm

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("journal/", include("journal.urls")),

    # Authentication
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),

    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]