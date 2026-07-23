from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    CivilServantSerializer,
    JobDetailSerializer,
    SalaryDetailSerializer,
    CivilServantCreateSerializer,
)
from .services.CivilServantService import (
    CivilServantService,
    JobDetailService,
    SalaryService,
)


class CivilServantView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get(self, request):
        queryset = CivilServantService.get_all_civil_servants()
        return Response(CivilServantSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = CivilServantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        civil_servant = CivilServantService.create_civil_servant(
            civil_servant_data=validated["civil_servant"],
            job_detail_data=validated["job_detail"],
            login_data=validated["login_data"],
        )

        return Response(
            CivilServantSerializer(civil_servant).data,
            status=status.HTTP_201_CREATED,
        )


class CivilServantPKView(APIView):

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = CivilServantService.get_civil_servant_with_id(id)
        elif CIN is not None:
            queryset = CivilServantService.get_civil_servant_with_CIN(CIN)

        return Response(CivilServantSerializer(queryset).data)

    def patch(self, request, id):
        serializer = CivilServantSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        civil_servant_updates = dict(serializer.validated_data)
        job_detail_updates = civil_servant_updates.pop("job_detail", None)

        updated_civil_servant = CivilServantService.update_civil_servant(
            civil_servant_id=id,
            civil_servant_updates=civil_servant_updates,
            job_detail_updates=job_detail_updates,
        )

        return Response(CivilServantSerializer(updated_civil_servant).data)


class JobDetailPKView(APIView):

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = JobDetailService.get_job_detail_with_id(id)
        elif CIN is not None:
            queryset = JobDetailService.get_job_detail_with_CIN(CIN)

        return Response(JobDetailSerializer(queryset).data)


class SalaryDetailPKView(APIView):

    def get(self, request, id=None, CIN=None):
        queryset = None
        if id is not None:
            queryset = SalaryService.get_salary_with_id(id)
        elif CIN is not None:
            queryset = SalaryService.get_salary_with_CIN(CIN)

        return Response(SalaryDetailSerializer(queryset).data)
