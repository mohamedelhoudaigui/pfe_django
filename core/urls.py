from django.urls import path
from .views import (
    CivilServantView,
    CivilServantPKView,
    JobDetailPKView,
    SalaryDetailPKView,
)

# router.register("civil-servant", CivilServantView, basename="civil-servant")

# router.register(
#     r"civil-servant/(?P<civil_servant_id>\d+)/job-detail",
#     JobDetailView,
#     basename="job-detail",
# )

# router.register(
#     r"civil-servant/(?P<civil_servant_id>\d+)/salary-detail",
#     SalaryDetailView,
#     basename="salary-detail",
# )
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
