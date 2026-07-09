from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import CivilServant, JobDetail, SalaryDetail
from .serializers import (
    CivilServantSerializer,
    JobDetailSerializer,
    SalaryDetailSerializer,
)
from .services.CivilServantService import CivilServantService


class CivilServantView(ModelViewSet):
    serializer_class = CivilServantSerializer
    queryset = CivilServant.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override create to use the service layer for orchestration.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract civil servant and job detail data
        civil_servant_data = {
            k: v for k, v in serializer.validated_data.items() if k != "job_detail"
        }
        job_detail_data = serializer.validated_data.get("job_detail")

        # Use service to create civil servant with job and salary
        try:
            civil_servant = (
                CivilServantService.create_civil_servant_with_job_and_salary(
                    civil_servant_data=civil_servant_data,
                    job_detail_data=job_detail_data,
                )
            )
            response_serializer = CivilServantSerializer(civil_servant)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Return optimized queryset with related objects."""
        return CivilServantService.get_all_civil_servants()


class JobDetailView(ModelViewSet):
    serializer_class = JobDetailSerializer

    def get_queryset(self):
        civil_servant_id = self.kwargs.get("civil_servant_id")
        if not civil_servant_id:
            return JobDetail.objects.none()
        return JobDetail.objects.filter(fonctionnaire=civil_servant_id)


class SalaryDetailView(ReadOnlyModelViewSet):
    serializer_class = SalaryDetailSerializer

    def get_queryset(self):
        civil_servant_id = self.kwargs.get("civil_servant_id")
        if not civil_servant_id:
            return SalaryDetail.objects.none()
        return SalaryDetail.objects.filter(civil_servant=civil_servant_id)
