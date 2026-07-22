from rest_framework import serializers
from .models import CivilServant, JobDetail, SalaryDetail
from django.contrib.auth.models import User


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
            "mutuelle",
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
        ]


class CivilServantSerializer(serializers.ModelSerializer):
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


class LoginDataSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value


# this is a wraper serializer for the creation of a civil servant
class CivilServantCreateSerializer(serializers.Serializer):
    civil_servant = CivilServantSerializer()
    job_detail = JobDetailSerializer()
    login_data = LoginDataSerializer()

    def validate(self, data):
        # cross-field validation across the three blocks, if needed
        return data
