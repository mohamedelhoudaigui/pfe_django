from rest_framework import serializers
from .models import CivilServant, JobDetail, SalaryDetail


class JobDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ["zone", "category", "grade", "echelon", "mutuelle"]


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = "__all__"


class SalaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDetail
        fields = "__all__"


class CivilServantSerializer(serializers.ModelSerializer):
    job_detail = JobDetailCreateSerializer(write_only=True, required=False)

    class Meta:
        model = CivilServant
        exclude = ["indemnities"]