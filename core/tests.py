from django.test import TestCase

from core.models import CivilServant, JobDetail, SalaryDetail
from core.serializers import CivilServantSerializer


class CivilServantSerializerTest(TestCase):
    def test_serializer_creates_job_and_salary_details(self):
        payload = {
            "CIN": "AA123456",
            "PPR": "PPR001",
            "nom": "Test",
            "prenom": "User",
            "date_de_naissance": "1990-01-01",
            "lieu_de_naissance": "Rabat",
            "genre": "man",
            "situation_familiale": "single",
            "n_enfants": 0,
            "address": "123 Main St",
            "job_detail": {
                "zone": "A",
                "category": "technicien",
                "grade": "1G",
                "echelon": 1,
                "mutuelle": "CNOPS",
            },
        }

        serializer = CivilServantSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        civil_servant = serializer.save()

        self.assertTrue(JobDetail.objects.filter(fonct=civil_servant).exists())
        self.assertTrue(SalaryDetail.objects.filter(civil_servant=civil_servant).exists())
