from django.urls import path

from . import views

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
]
