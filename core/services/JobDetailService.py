from ..models import CivilServant, JobDetail
from django.shortcuts import get_object_or_404


class JobDetailService:
    """Service for managing job detail business logic."""

    # Full index table of civil servant categories
    ECHELON_INDICE_TABLEAU = {
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
        "administrateur": {
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
        "adjoint_administratif": {
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
        "ingenieur_application": {
            "grade_principal": {
                1: 402,
                2: 428,
                3: 456,
                4: 484,
                5: 512,
                6: 564,
            },
            "1G": {
                1: 275,
                2: 300,
                3: 326,
                4: 351,
                5: 377,
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
        "sage_femme": {
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
        "kinesitherapeute": {
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
        "assistant_medico_social": {
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
            "specialiste_hors_grade": {
                1: 509,
                2: 542,
                3: 575,
                4: 608,
                5: 641,
            },
            "specialiste_grade_exceptionnelle": {
                1: 674,
                2: 707,
                3: 740,
                4: 773,
                5: 806,
            },
            "specialiste_grade_principal": {
                1: 770,
                2: 799,
                3: 839,
                4: 872,
                5: 905,
            },
            "specialiste_1G": {
                1: 869,
                2: 899,
                3: 938,
                4: 971,
                5: 1004,
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
            "specialiste_1G": {
                1: 509,
                2: 542,
                3: 575,
                4: 608,
                5: 641,
            },
            "specialiste_grade_principal": {
                1: 674,
                2: 707,
                3: 740,
                4: 773,
                5: 806,
            },
            "specialiste_grade_exceptionnelle": {
                1: 770,
                2: 799,
                3: 839,
                4: 872,
                5: 905,
            },
            "specialiste_hors_grade": {
                1: 869,
                2: 899,
                3: 938,
                4: 971,
                5: 1004,
            },
        },
        "pharmacien": {
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
            "specialiste_1G": {
                1: 509,
                2: 542,
                3: 575,
                4: 608,
                5: 641,
            },
            "specialiste_grade_principal": {
                1: 674,
                2: 707,
                3: 740,
                4: 773,
                5: 806,
            },
            "specialiste_grade_exceptionnelle": {
                1: 770,
                2: 799,
                3: 839,
                4: 872,
                5: 905,
            },
            "specialiste_hors_grade": {
                1: 869,
                2: 899,
                3: 938,
                4: 971,
                5: 1004,
            },
        },
        "chirurgien_dentiste": {
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
            "specialiste_1G": {
                1: 509,
                2: 542,
                3: 575,
                4: 608,
                5: 641,
            },
            "specialiste_grade_principal": {
                1: 674,
                2: 707,
                3: 740,
                4: 773,
                5: 806,
            },
            "specialiste_grade_exceptionnelle": {
                1: 770,
                2: 799,
                3: 839,
                4: 872,
                5: 905,
            },
            "specialiste_hors_grade": {
                1: 869,
                2: 899,
                3: 938,
                4: 971,
                5: 1004,
            },
        },
        "professeur_de_enseignement_superieur": {
            "grade_A": {
                1: 760,
                2: 785,
                3: 810,
                4: 835,
            },
            "grade_B": {
                1: 860,
                2: 885,
                3: 915,
                4: 945,
            },
            "grade_C": {
                1: 975,
                2: 1005,
                3: 1035,
                4: 1065,
            },
            "grade_D": {
                1: 1095,
                2: 1125,
                3: 1155,
                4: 1185,
                5: 1215,
            },
        },
        "maitre_de_conference_habilite": {
            "grade_A": {
                1: 580,
                2: 620,
                3: 660,
                4: 720,
            },
            "grade_B": {
                1: 779,
                2: 812,
                3: 840,
                4: 870,
            },
            "grade_C": {
                1: 900,
                2: 930,
                3: 960,
                4: 990,
                5: 1020,
            },
        },
        "maitre_de_conference": {
            "grade_A": {
                1: 509,
                2: 542,
                3: 574,
                4: 606,
            },
            "grade_B": {
                1: 639,
                2: 704,
                3: 746,
                4: 779,
            },
            "grade_C": {
                1: 812,
                2: 840,
                3: 870,
                4: 900,
            },
            "grade_D": {
                1: 930,
                2: 960,
                3: 990,
                4: 1020,
            },
        },
        "professeur": {
            "1G": {
                1: 704,
                2: 746,
                3: 779,
                4: 812,
                5: 840,
                6: 870,
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
                # 11 = exceptionnelle
            },
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
        },
        "chef_de_travaux": {
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
            "2G": {
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
            "3G": {
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
        "inspecteur_de_la_formation_professionnelle": {
            "1G": {
                1: 704,
                2: 746,
                3: 779,
                4: 812,
                5: 840,
                6: 870,
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
                # 11 = exceptionnelle
            },
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
        },
        "cadre_des_conseillers_en_orientation_et_en_planification_professionnelle": {
            "grade_principal": {
                1: 704,
                2: 746,
                3: 779,
                4: 812,
                5: 840,
                6: 870,
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
                11: 704,
                # 11 = exceptionnelle
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
        },
        "maitre_assistant": {
            "grade_A": {
                1: 336,
                2: 369,
                3: 403,
                4: 436,
                5: 472,
            },
            "grade_B": {
                1: 509,
                2: 542,
                3: 573,
                4: 606,
                5: 639,
                6: 704,
            },
            "grade_C": {
                1: 746,
                2: 779,
                3: 812,
                4: 840,
            },
        },
        "assistant": {
            "grade_A": {
                1: 326,
                2: 351,
                3: 377,
                4: 402,
                5: 428,
            },
            "grade_B": {
                1: 472,
                2: 509,
                3: 542,
                4: 574,
                5: 606,
                6: 639,
                7: 680,
            },
        },
    }

    @staticmethod
    def get_jobdetail(civil_servant: CivilServant) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant=civil_servant)

    @staticmethod
    def get_job_detail_with_id(id: int) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant__id=id)

    @staticmethod
    def get_job_detail_with_CIN(cin: str) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant__CIN=cin)

    @staticmethod
    def calculate_indice(categorie: str, grade: str, echelon: int) -> int:
        """
        Calculate the indice based on categorie, grade and echelon.

        Args:
            categorie: The categorie of the civil servant (e.g, 'technicien',...)
            grade: The grade code (e.g., '4G', '3G', '2G', '1G')
            echelon: The echelon level (1-13)

        Returns:
            The calculated indice value

        Raises:
            ValueError: If grade or echelon is invalid
        """
        if categorie not in JobDetailService.ECHELON_INDICE_TABLEAU:
            raise ValueError(f"Invalid categorie: {grade}")

        categorie_table = JobDetailService.ECHELON_INDICE_TABLEAU[categorie]
        if grade not in categorie_table:
            raise ValueError(f"Invalid grade {grade} for categorie {categorie}")

        grade_table = categorie_table[grade]
        if echelon not in grade_table:
            raise ValueError(f"Invalid echelon {echelon} for grade {grade}")

        return grade_table[echelon]

    @staticmethod
    def save_job_detail(civil_servant, job_detail_data: dict) -> JobDetail:
        """
        Create or update a JobDetail, recalculating indice if grade/echelon change.
        """
        job_detail = JobDetail.objects.filter(civil_servant=civil_servant).first()
        created = job_detail is None

        if created:
            job_detail = JobDetail(civil_servant=civil_servant)

        for key, value in job_detail_data.items():
            setattr(job_detail, key, value)

        if created or "grade" in job_detail_data or "echelon" in job_detail_data:
            job_detail.indice = JobDetailService.calculate_indice(
                job_detail.grade, job_detail.echelon
            )

        job_detail.save()
        return job_detail
