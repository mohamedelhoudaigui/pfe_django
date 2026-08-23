import random
from typing import Dict

from django.db import transaction
from faker import Faker

from ..models import Categorie, Grade, EchelonIndice
from .CivilServantService import CivilServantService


class SeedService:
    """Seeds reference data (categorie/grade/indice) and fake demo data."""

    # ---- reference data source of truth ----
    ECHELON_INDICE_TABLEAU: Dict = {
		"technicien": {
			"4G": {
				1: 207,
				2: 224,
				3: 241,
				4: 259,
				5: 276,
				6: 293,
				7: 311,
				8: 332,
				9: 353,
				10: 373,
			},
			"3G": {
				1: 235,
				2: 253,
				3: 274,
				4: 296,
				5: 317,
				6: 339,
				7: 361,
				8: 382,
				9: 404,
				10: 438,
			},
			"2G": {
				1: 275,
				2: 300,
				3: 326,
				4: 351,
				5: 377,
				6: 402,
				7: 428,
				8: 456,
				9: 484,
				10: 512,
				11: 564,
				# 11 = exceptionnelle
			},
			"1G": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
				6: 509,
				7: 542,
				8: 574,
				9: 606,
				10: 639,
				11: 675,
				12: 690,
				13: 704,
			},
		},
		"administrateur_IM": {
			"3G": {
				1: 275,
				2: 300,
				3: 326,
				4: 351,
				5: 377,
				6: 402,
				7: 428,
				8: 456,
				9: 484,
				10: 512,
				11: 564,
				# 11 = exceptionnelle
			},
			"2G": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
				6: 509,
				7: 542,
				8: 574,
				9: 606,
				10: 639,
				11: 704,
			},
			"1G": {
				1: 704,
				2: 746,
				3: 779,
				4: 812,
				5: 840,
				6: 860,
			},
		},
		"adjoint_technique": {
			"1G": {
				1: 207,
				2: 224,
				3: 241,
				4: 259,
				5: 276,
				6: 293,
				7: 311,
				8: 332,
				9: 353,
				10: 373,
			},
			"2G": {
				1: 153,
				2: 161,
				3: 173,
				4: 185,
				5: 197,
				6: 209,
				7: 222,
				8: 236,
				9: 249,
				10: 262,
			},
			"grade_principal": {
				1: 235,
				2: 253,
				3: 274,
				4: 296,
				5: 317,
				6: 339,
				7: 361,
				8: 382,
				9: 404,
				10: 438,
			},
		},
		"adjoint_administratif_IM": {
			"1G": {
				1: 207,
				2: 224,
				3: 241,
				4: 259,
				5: 276,
				6: 293,
				7: 311,
				8: 332,
				9: 353,
				10: 373,
			},
			"2G": {
				1: 153,
				2: 161,
				3: 173,
				4: 185,
				5: 197,
				6: 209,
				7: 222,
				8: 236,
				9: 249,
				10: 262,
			},
			"grade_principal": {
				1: 235,
				2: 253,
				3: 274,
				4: 296,
				5: 317,
				6: 339,
				7: 361,
				8: 382,
				9: 404,
				10: 438,
			},
		},
		"redacteur": {
			"1G": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
				6: 509,
				7: 542,
				8: 574,
				9: 606,
				10: 639,
				11: 675,
				12: 690,
				13: 704,
			},
			"2G": {
				1: 275,
				2: 300,
				3: 326,
				4: 351,
				5: 377,
				6: 402,
				7: 428,
				8: 456,
				9: 484,
				10: 512,
				11: 564,
			},
			"3G": {
				1: 235,
				2: 253,
				3: 274,
				4: 296,
				5: 317,
				6: 339,
				7: 361,
				8: 382,
				9: 404,
				10: 438,
			},
			"4G": {
				1: 207,
				2: 224,
				3: 241,
				4: 259,
				5: 276,
				6: 293,
				7: 311,
				8: 332,
				9: 353,
				10: 373,
			},
		},
		"ingenieur_en_chef": {
			"grade_principal": {
				1: 870,
				2: 900,
				3: 930,
				4: 960,
				5: 990,
			},
			"1G": {
				1: 704,
				2: 746,
				3: 779,
				4: 812,
				5: 840,
				6: 870,
			},
		},
		"ingenieur_etat": {
			"grade_principal": {
				1: 509,
				2: 542,
				3: 574,
				4: 606,
				5: 639,
				6: 704,
			},
			"1G": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
			},
		},
		"architect_en_chef": {
			"grade_principal": {
				1: 870,
				2: 900,
				3: 930,
				4: 960,
				5: 990,
			},
			"1G": {
				1: 704,
				2: 746,
				3: 779,
				4: 812,
				5: 840,
				6: 870,
			},
		},
		"architect": {
			"grade_principal": {
				1: 509,
				2: 542,
				3: 574,
				4: 606,
				5: 639,
				6: 704,
			},
			"1G": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
			},
		},
		"infirmier": {
			"grade_exceptionnelle": {
				1: 704,
				2: 746,
				3: 779,
				4: 812,
				5: 840,
				6: 870,
			},
			"grade_principal": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
				6: 509,
				7: 542,
				8: 574,
				9: 606,
				10: 639,
				11: 675,
				12: 690,
				13: 704,
			},
			"1G": {
				1: 275,
				2: 300,
				3: 326,
				4: 351,
				5: 377,
				6: 402,
				7: 428,
				8: 456,
				9: 484,
				10: 512,
				11: 564,
			},
		},
		"technicien_de_sante": {
			"grade_exceptionnelle": {
				1: 704,
				2: 746,
				3: 779,
				4: 812,
				5: 840,
				6: 870,
			},
			"grade_principal": {
				1: 336,
				2: 369,
				3: 403,
				4: 436,
				5: 472,
				6: 509,
				7: 542,
				8: 574,
				9: 606,
				10: 639,
				11: 675,
				12: 690,
				13: 704,
			},
			"1G": {
				1: 275,
				2: 300,
				3: 326,
				4: 351,
				5: 377,
				6: 402,
				7: 428,
				8: 456,
				9: 484,
				10: 512,
				11: 564,
				# 11 = exceptionnelle
			},
		},
		"medecine_veterinaire": {
			"hors_grade": {
				1: 869,
				2: 899,
				3: 938,
				4: 971,
				5: 1004,
			},
			"grade_exceptionnelle": {
				1: 770,
				2: 799,
				3: 839,
				4: 872,
				5: 905,
			},
			"grade_principal": {
				1: 674,
				2: 707,
				3: 740,
				4: 773,
				5: 806,
			},
			"1G": {
				1: 509,
				2: 542,
				3: 575,
				4: 608,
				5: 641,
			},
		},
		"medecin": {
			"hors_grade": {
				1: 869,
				2: 899,
				3: 938,
				4: 971,
				5: 1004,
			},
			"grade_exceptionnelle": {
				1: 770,
				2: 799,
				3: 839,
				4: 872,
				5: 905,
			},
			"grade_principal": {
				1: 674,
				2: 707,
				3: 740,
				4: 773,
				5: 806,
			},
			"1G": {
				1: 509,
				2: 542,
				3: 575,
				4: 608,
				5: 641,
			},
		},
	}

    # ---- reference data seeding ----

    @staticmethod
    def is_reference_data_seeded() -> bool:
        """Quick check: has the categorie/grade/indice table already been populated?"""
        return Categorie.objects.exists()

    @staticmethod
    @transaction.atomic
    def seed_categorie_grade_indice(force: bool = False) -> dict:
        """
        Idempotently seed Categorie/Grade/EchelonIndice from ECHELON_INDICE_TABLEAU.

        - Fresh project (no Categorie rows yet): inserts everything.
        - Existing project: skips entirely unless force=True.
        - Even with force=True, get_or_create means no duplicates are ever created.
        """
        if not force and SeedService.is_reference_data_seeded():
            return {"skipped": True, "categorie": 0, "grade": 0, "echelon_indice": 0}

        counts = {"skipped": False, "categorie": 0, "grade": 0, "echelon_indice": 0}

        for categorie_code, grades in SeedService.ECHELON_INDICE_TABLEAU.items():
            categorie, cat_created = Categorie.objects.get_or_create(
                code=categorie_code,
                defaults={"label": categorie_code.replace("_", " ").title()},
            )
            counts["categorie"] += int(cat_created)

            for grade_code, echelons in grades.items():
                grade, grade_created = Grade.objects.get_or_create(
                    categorie=categorie,
                    code=grade_code,
                    defaults={"label": grade_code},
                )
                counts["grade"] += int(grade_created)

                for echelon, indice in echelons.items():
                    _, ei_created = EchelonIndice.objects.get_or_create(
                        grade=grade,
                        echelon=echelon,
                        defaults={"indice": indice},
                    )
                    counts["echelon_indice"] += int(ei_created)

        return counts

    # ---- fake demo data (moved from root seed.py) ----

    GRADE_ECHELON_MAP = {
        "4G": range(1, 11),
        "3G": range(1, 11),
        "2G": range(1, 12),
        "1G": range(1, 14),
    }
    ECHELLE_SEQ = list(range(1, 13))
    VILLES = ["Rabat", "Casablanca", "Fès", "Marrakech", "Tanger", "Agadir", "Meknès", "Oujda", "Larache"]

    @staticmethod
    def _build_fake_payload(fake: Faker, index: int) -> list:
        grade = random.choice(["1G", "2G", "3G", "4G"])
        return [
            {
                "CIN": f"LA{fake.unique.numerify('######')}",
                "PPR": f"PPR{fake.unique.numerify('#######')}",
                "nom": fake.last_name(),
                "prenom": fake.first_name(),
                "date_de_naissance": fake.date_of_birth(minimum_age=25, maximum_age=60),
                "lieu_de_naissance": random.choice(SeedService.VILLES),
                "genre": random.choice(["man", "woman"]),
                "situation_familiale": random.choice(["single", "married", "divorced"]),
                "n_enfants": random.randint(0, 5),
                "address": fake.address(),
            },
            {
                "zone": random.choice(["A", "B", "C"]),
                "categorie": "technicien",
                "grade": grade,
                "echelle": random.choice(SeedService.ECHELLE_SEQ),
                "echelon": random.choice(list(SeedService.GRADE_ECHELON_MAP[grade])),
                "mutuelle": "CNOPS",
            },
            {
                "username": fake.unique.user_name(),
                "email": fake.unique.email(),
                "password": "test@123",
            },
        ]

    @staticmethod
    def seed_fake_civil_servants(count: int = 20) -> int:
        """Generate `count` fake civil servants with job/salary details. Not idempotent by design — call once."""
        fake = Faker("en_US")
        created = 0
        for i in range(count):
            payload = SeedService._build_fake_payload(fake, i)
            CivilServantService.create_civil_servant(
                civil_servant_data=payload[0],
                job_detail_data=payload[1],
                login_data=payload[2],
            )
            created += 1
        return created