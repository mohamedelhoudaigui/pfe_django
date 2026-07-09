from rest_framework import serializers
from .models import CivilServant, JobDetail, SalaryDetail


class JobDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ["zone", "categorie", "grade", "echelle", "echelon", "mutuelle"]


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = [
            "id",
            "zone",
            "categorie",
            "grade",
            "echelle",
            "echelon",
            "indice",
            "mutuelle",
            "created_at",
            "updated_at",
        ]


class SalaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDetail
        fields = [
            "id",
            "base_salary",
            # "indemnities",
            "tsp",
            "family_allowance",
            "annual_gross_salary",
            "monthly_gross_salary",
            "cmr",
            "amo",
            "sm",
            "ccd",
            "fos",
            "income_tax",
            "net_salary",
            "created_at",
            "updated_at",
        ]


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
            "created_at",
            "updated_at",
        ]
