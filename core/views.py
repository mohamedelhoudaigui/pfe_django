from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import CivilServant, JobDetail, SalaryDetail
from .serializers import (
    CivilServantSerializer,
    JobDetailSerializer,
    SalaryDetailSerializer,
)


class CivilServantView(ModelViewSet):
    serializer_class = CivilServantSerializer
    queryset = CivilServant.objects.all()


class JobDetailView(ModelViewSet):
    serializer_class = JobDetailSerializer

    def get_queryset(self):
        civil_servant_id = self.kwargs.get("civil_servant_id")
        if not civil_servant_id:
            return JobDetail.objects.none()
        return JobDetail.objects.filter(fonct=civil_servant_id)


class SalaryDetailView(ReadOnlyModelViewSet):
    serializer_class = SalaryDetailSerializer

    def get_queryset(self):
        civil_servant_id = self.kwargs.get("civil_servant_id")
        if not civil_servant_id:
            return SalaryDetail.objects.none()
        return SalaryDetail.objects.filter(civil_servant=civil_servant_id)
