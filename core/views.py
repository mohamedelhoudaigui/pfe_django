from rest_framework.viewsets import ModelViewSet
from .serializers import CivilServantSerializer, JobDetailerializer
from .models import CivilServant, JobDetail

# Create your views here.


class CivilServantView(ModelViewSet):
    serializer_class = CivilServantSerializer
    queryset = CivilServant.objects.all()


class JobDetailView(ModelViewSet):
    serializer_class = JobDetailerializer

    def get_queryset(self):
        civil_servant_id = self.kwargs.get("civil_servant_id")
        if not civil_servant_id:
            return JobDetail.objects.none()
        return JobDetail.objects.filter(fonct=civil_servant_id)
