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
            },  # 11 = exceptionnelle
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
            "principal": {
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
            "principal": {
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
