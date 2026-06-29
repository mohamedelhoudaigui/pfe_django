from rest_framework.routers import DefaultRouter
from .views import CivilServantView, JobDetailView

router = DefaultRouter()
router.register("civil-servant", CivilServantView, basename="civil-servant")

router.register(
    r"civil-servant/(?P<civil_servant_id>\d+)/job-detail",
    JobDetailView,
    basename="job-detail",
)

urlpatterns = router.urls
