import os
import random
import uuid
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commune_project.settings")
django.setup()

from core.services.CivilServantService import CivilServantService

fake = Faker("en_US")

GRADE_ECHELON_MAP = {
    "4G": range(1, 11),
    "3G": range(1, 11),
    "2G": range(1, 12),
    "1G": range(1, 14),
}

ECHELLE_SEQ = [i for i in range(1, 13)]


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
            "categorie": "technicien",
            "grade": grade,
            "echelle": random.choice(ECHELLE_SEQ),
            "echelon": random.choice(list(GRADE_ECHELON_MAP[grade])),
            "mutuelle": "CNOPS",
        },
    }


if __name__ == "__main__":
    COUNT = 20

    print(f"Creating {COUNT} civil servants with linked job and salary details...")

    for _ in range(COUNT):
        payload = build_payload()
        civil_servant_data = {
            "CIN": payload["CIN"],
            "PPR": payload["PPR"],
            "nom": payload["nom"],
            "prenom": payload["prenom"],
            "date_de_naissance": payload["date_de_naissance"],
            "lieu_de_naissance": payload["lieu_de_naissance"],
            "genre": payload["genre"],
            "situation_familiale": payload["situation_familiale"],
            "n_enfants": payload["n_enfants"],
            "address": payload["address"],
        }
        job_detail_data = payload["job_detail"]

        CivilServantService.create_civil_servant(
            civil_servant_data=civil_servant_data,
            job_detail_data=job_detail_data,
        )

    print(f"✅ Done! {COUNT} civil servants created with job and salary details.")
