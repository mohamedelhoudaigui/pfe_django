from ..models import CivilServant, JobDetail
from django.shortcuts import get_object_or_404


class JobDetailService:
    """Service for managing job detail business logic."""

    # Full index table from the PDF (grade -> rank -> index)
    ECHELON_INDICE_TABLEAU = {
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
    }

    @staticmethod
    def get_jobdetail(civil_servant: CivilServant) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant=civil_servant)

    @staticmethod
    def get_job_detail_with_id(id: int) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant__id=id)

    @staticmethod
    def get_job_detail_with_cin(cin: str) -> JobDetail:
        return get_object_or_404(JobDetail, civil_servant__CIN=cin)

    @staticmethod
    def calculate_indice(grade: str, echelon: int) -> int:
        """
        Calculate the indice based on grade and echelon.

        Args:
            grade: The grade code (e.g., '4G', '3G', '2G', '1G')
            echelon: The echelon level (1-13)

        Returns:
            The calculated indice value

        Raises:
            ValueError: If grade or echelon is invalid
        """
        if grade not in JobDetailService.ECHELON_INDICE_TABLEAU:
            raise ValueError(f"Invalid grade: {grade}")

        grade_table = JobDetailService.ECHELON_INDICE_TABLEAU[grade]
        if echelon not in grade_table:
            raise ValueError(f"Invalid echelon {echelon} for grade {grade}")

        return grade_table[echelon]

    @staticmethod
    def create_job_detail(civil_servant, job_detail_data: dict) -> JobDetail:
        """
        Create a JobDetail with calculated indice.

        Args:
            civil_servant: CivilServant instance
            job_detail_data: Dict with keys zone, categorie, grade,
                echelle, echelon, mutuelle

        Returns:
            Created JobDetail instance

        Raises:
            ValueError: If validation fails
        """
        indice = JobDetailService.calculate_indice(
            job_detail_data["grade"], job_detail_data["echelon"]
        )

        job_detail = JobDetail(
            civil_servant=civil_servant,
            indice=indice,
            **job_detail_data,
        )
        job_detail.save()

        return job_detail

    @staticmethod
    def update_job_detail(job_detail: JobDetail, job_detail_updates: dict) -> JobDetail:
        """
        Update a JobDetail and recalculate indice if grade/echelon change.

        Args:
            job_detail: JobDetail instance to update
            job_detail_updates: Dict with any subset of zone, categorie,
                grade, echelle, echelon, mutuelle

        Returns:
            Updated JobDetail instance

        Raises:
            ValueError: If validation fails
        """
        for key, value in job_detail_updates.items():
            setattr(job_detail, key, value)

        # If grade or echelon changed, recalculate indice
        if "grade" in job_detail_updates or "echelon" in job_detail_updates:
            job_detail.indice = JobDetailService.calculate_indice(
                job_detail.grade, job_detail.echelon
            )

        job_detail.save()
        return job_detail
