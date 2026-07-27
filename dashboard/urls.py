# dashboard/urls.py
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "civil-servants/register/",
        views.civil_servant_register,
        name="civil_servant_register",
    ),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("civil-servants/", views.civil_servant_list, name="civil_servant_list"),
    path(
        "civil-servants/<int:pk>/",
        views.civil_servant_detail,
        name="civil_servant_detail",
    ),
    path(
        "civil-servants/search/",
        views.civil_servant_search,
        name="civil_servant_search",
    ),
]
