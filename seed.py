import os
import django
import random
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commune_project.settings")
django.setup()

import factory
from faker import Faker
from core.models import CivilServant, JobDetail

fake = Faker("en_US")

# ─────────────────────────────────────────
# CivilServant Factory
# ─────────────────────────────────────────


class CivilServantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CivilServant

    CIN = factory.LazyFunction(lambda: f"LA{uuid.uuid4().hex[:6].upper()}")
    PPR = factory.LazyFunction(lambda: f"PPR{uuid.uuid4().hex[:7].upper()}")
    nom = factory.LazyFunction(lambda: fake.last_name())
    prenom = factory.LazyFunction(lambda: fake.first_name())
    date_de_naissance = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=25, maximum_age=60)
    )
    lieu_de_naissance = factory.LazyFunction(
        lambda: random.choice(
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
        )
    )
    genre = factory.LazyFunction(lambda: random.choice(["man", "woman"]))
    situation_familiale = factory.LazyFunction(
        lambda: random.choice(["single", "married", "divorced"])
    )
    n_enfants = factory.LazyFunction(lambda: random.randint(0, 5))
    address = factory.LazyFunction(lambda: fake.address())


# ─────────────────────────────────────────
# JobDetail Factory
# ─────────────────────────────────────────

# Valid echelon ranges per grade (based on ECHELON_INDICE_TABLEAU)
GRADE_ECHELON_MAP = {
    "4G": range(1, 11),  # echelons 1–10
    "3G": range(1, 11),  # echelons 1–10
    "2G": range(1, 12),  # echelons 1–11
    "1G": range(1, 14),  # echelons 1–13
}


class JobDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobDetail

    fonct = factory.SubFactory(CivilServantFactory)
    zone = factory.LazyFunction(lambda: random.choice(["A", "B", "C"]))
    category = factory.LazyFunction(
        lambda: "technicien"
    )  # ✅ matches CATEGORIES choices
    grade = factory.LazyFunction(lambda: random.choice(["1G", "2G", "3G", "4G"]))
    echelon = factory.LazyAttribute(
        lambda obj: random.choice(list(GRADE_ECHELON_MAP[obj.grade]))
    )
    mutuelle = factory.LazyFunction(
        lambda: "CNOPS"
    )  # ✅ fixed typo 'mutelle' → 'mutuelle', matches MUTUELLE choices


# ─────────────────────────────────────────
# Seed the database
# ─────────────────────────────────────────

if __name__ == "__main__":
    COUNT = 20  # change this to however many records you want

    print(f"Creating {COUNT} civil servants with job details...")

    for _ in range(COUNT):
        JobDetailFactory()  # also creates a CivilServant via SubFactory

    print(f"✅ Done! {COUNT} records inserted.")
