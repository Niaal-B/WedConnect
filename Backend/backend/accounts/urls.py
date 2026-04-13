from django.urls import path
from .views import AdminLoginView, AdminLogoutView, AdminMeView

app_name = "accounts"

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("logout/", AdminLogoutView.as_view(), name="admin-logout"),
    path("me/", AdminMeView.as_view(), name="admin-me"),
]