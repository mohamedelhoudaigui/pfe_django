from django.db import transaction
from rest_framework import serializers
from .models import CivilServant, JobDetail, SalaryDetail
from .services.salary import SalaryService


class JobDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ["zone", "category", "grade", "echelon", "mutuelle"]


class CivilServantSerializer(serializers.ModelSerializer):
    job_detail = JobDetailCreateSerializer(write_only=True, required=False)

    class Meta:
        model = CivilServant
        fields = [
            "id",
            "CIN",
            "PPR",
            "nom",
            "prenom",
            "date_de_naissance",
            "lieu_de_naissance",
            "genre",
            "situation_familiale",
            "n_enfants",
            "address",
            "job_detail",
        ]

    def create(self, validated_data):
        job_detail_data = validated_data.pop("job_detail", None)

        with transaction.atomic():
            civil_servant = CivilServant.objects.create(**validated_data)

            if job_detail_data:
                job_detail = JobDetail.objects.create(
                    fonct=civil_servant,
                    **job_detail_data,
                )
                SalaryService(civil_servant, job_detail).save_to_model()

            return civil_servant


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        exclude = ["id", "created_at", "updated_at"]


class SalaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDetail
        exclude = ["id", "income_reduction", "taxable_income"]
