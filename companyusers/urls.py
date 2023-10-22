from django.urls import path

from . import views
from .api import views as api_views

app_name = "companyusers"

urlpatterns = [
    # ------ user related urls ------
    path("", views.user_login, name="user_login"),
    path("register/", views.user_register, name="user_register"),
    path("logout/", views.user_logout, name="user_logout"),
    path("home/", views.user_home, name="user_home"),
    # ------ company related urls ------
    path("company-list/", views.company_list, name="company_list"),
    path("company/<slug:slug>/", views.company_detail, name="company_detail"),
    # --------- api urls ---------
    path(
        "api/user-list/", api_views.UserListAPIView.as_view(), name="user_list_api"
    ),
    path(
        "api/user-detail/",
        api_views.UserDetailAPIView.as_view(
            {"get": "retrieve", "put": "update", "post": "create"}
        ),
        name="user_detail_api",
    ),
]
