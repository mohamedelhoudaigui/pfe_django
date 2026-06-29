from rest_framework import serializers
from .models import CivilServant, JobDetail


class CivilServantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilServant
        exclude = ["id", "created_at", "updated_at"]


class JobDetailerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        exclude = ["id", "fonct", "created_at", "updated_at"]
