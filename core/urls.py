from django.urls import path
from .views import (
    CivilServantView,
    CivilServantPKView,
    JobDetailPKView,
    SalaryDetailPKView,
)

urlpatterns = [
    path("civil-servant/", CivilServantView.as_view(), name="civil-servant-list"),
    path(
        "civil-servant/<int:id>/",
        CivilServantPKView.as_view(),
        name="civil-servant-by-id",
    ),
    path(
        "civil-servant/<str:CIN>/",
        CivilServantPKView.as_view(),
        name="civil-servant-by-cin",
    ),
    path(
        "civil-servant/<int:id>/job-detail",
        JobDetailPKView.as_view(),
        name="job-detail-by-id",
    ),
    path(
        "civil-servant/<str:CIN>/job-detail",
        JobDetailPKView.as_view(),
        name="job-detail-by-cin",
    ),
    path(
        "civil-servant/<int:id>/salary-detail",
        SalaryDetailPKView.as_view(),
        name="salary-detail-by-id",
    ),
    path(
        "civil-servant/<str:CIN>/salary-detail",
        SalaryDetailPKView.as_view(),
        name="salary-detail-by-cin",
    ),
]
