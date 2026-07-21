from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CivilServantSerializer,
    JobDetailSerializer,
    SalaryDetailSerializer,
)
from .services.CivilServantService import (
    CivilServantService,
    JobDetailService,
    SalaryService,
)


class CivilServantView(APIView):
    serializer_class = CivilServantSerializer

    def get(self, request):
        queryset = CivilServantService.get_all_civil_servants()
        return Response(self.serializer_class(queryset, many=True).data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        civil_servant_data = dict(serializer.validated_data)
        job_detail_data = civil_servant_data.pop("job_detail", None)

        queryset = CivilServantService.create_civil_servant_with_job_and_salary(
            civil_servant_data=civil_servant_data,
            job_detail_data=job_detail_data,
        )

        return Response(
            self.serializer_class(queryset).data, status=status.HTTP_201_CREATED
        )


class CivilServantPKView(APIView):
    serializer_class = CivilServantSerializer

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = CivilServantService.get_civil_servant_with_id(id)
        elif CIN is not None:
            queryset = CivilServantService.get_civil_servant_with_CIN(CIN)
        if not queryset:
            return Response()
        return Response(self.serializer_class(queryset).data)

    def patch(self, request, id):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        civil_servant_updates = dict(serializer.validated_data)
        job_detail_updates = civil_servant_updates.pop("job_detail", None)

        updated_civil_servant = CivilServantService.update_civil_servant(
            civil_servant_id=id,
            civil_servant_updates=civil_servant_updates,
            job_detail_updates=job_detail_updates,
        )

        return Response(self.serializer_class(updated_civil_servant).data)


class JobDetailPKView(APIView):
    serializer_class = JobDetailSerializer

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = JobDetailService.get_job_detail_with_id(id)
        elif CIN is not None:
            queryset = JobDetailService.get_job_detail_with_CIN(CIN)

        return Response(self.serializer_class(queryset).data)


class SalaryDetailPKView(APIView):
    serializer_class = SalaryDetailSerializer

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = SalaryService.get_salary_with_id(id)
        elif CIN is not None:
            queryset = SalaryService.get_salary_with_CIN(CIN)

        return Response(self.serializer_class(queryset).data)
