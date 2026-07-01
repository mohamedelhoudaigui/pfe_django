import os
import random
import uuid
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commune_project.settings")
django.setup()

from core.serializers import CivilServantSerializer

fake = Faker("en_US")

GRADE_ECHELON_MAP = {
    "4G": range(1, 11),
    "3G": range(1, 11),
    "2G": range(1, 12),
    "1G": range(1, 14),
}


def build_payload():
    grade = random.choice(["1G", "2G", "3G", "4G"])
    return {
        "CIN": f"LA{uuid.uuid4().hex[:6].upper()}",
        "PPR": f"PPR{uuid.uuid4().hex[:7].upper()}",
        "nom": fake.last_name(),
        "prenom": fake.first_name(),
        "date_de_naissance": fake.date_of_birth(minimum_age=25, maximum_age=60),
        "lieu_de_naissance": random.choice(
            [
                "Rabat",
                "Casablanca",
                "Fès",
                "Marrakech",
                "Tanger",
                "Agadir",
                "Meknès",
                "Oujda",
                "Larache",
            ]
        ),
        "genre": random.choice(["man", "woman"]),
        "situation_familiale": random.choice(["single", "married", "divorced"]),
        "n_enfants": random.randint(0, 5),
        "address": fake.address(),
        "job_detail": {
            "zone": random.choice(["A", "B", "C"]),
            "category": "technicien",
            "grade": grade,
            "echelon": random.choice(list(GRADE_ECHELON_MAP[grade])),
            "mutuelle": "CNOPS",
        },
    }


if __name__ == "__main__":
    COUNT = 20

    print(f"Creating {COUNT} civil servants with linked job and salary details...")

    for _ in range(COUNT):
        payload = build_payload()
        serializer = CivilServantSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    print(f"✅ Done! {COUNT} civil servants created with job and salary details.")
