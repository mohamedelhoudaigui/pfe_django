from ..models import CivilServant, JobDetail


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
        job_detail = JobDetail.objects.get(fonct=civil_servant)
        return job_detail

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
    def create_job_detail(
        civil_servant, zone: str, category: str, grade: str, echelon: int, mutuelle: str
    ) -> JobDetail:
        """
        Create a JobDetail with calculated indice.

        Args:
            civil_servant: CivilServant instance
            zone: Zone code ('A', 'B', or 'C')
            category: Job category
            grade: Grade code ('4G', '3G', '2G', '1G')
            echelon: Echelon level (1-13)
            mutuelle: Mutuelle code

        Returns:
            Created JobDetail instance

        Raises:
            ValueError: If validation fails
        """
        indice = JobDetailService.calculate_indice(grade, echelon)

        job_detail = JobDetail(
            fonct=civil_servant,
            zone=zone,
            category=category,
            grade=grade,
            echelon=echelon,
            indice=indice,
            mutuelle=mutuelle,
        )
        job_detail.save()
        return job_detail

    @staticmethod
    def update_job_detail(
        job_detail: JobDetail,
        zone: str = None,
        category: str = None,
        grade: str = None,
        echelon: int = None,
        mutuelle: str = None,
    ) -> JobDetail:
        """
        Update a JobDetail and recalculate indice if grade/echelon change.

        Args:
            job_detail: JobDetail instance to update
            zone: New zone (optional)
            category: New category (optional)
            grade: New grade (optional)
            echelon: New echelon (optional)
            mutuelle: New mutuelle (optional)

        Returns:
            Updated JobDetail instance

        Raises:
            ValueError: If validation fails
        """
        if zone is not None:
            job_detail.zone = zone
        if category is not None:
            job_detail.category = category
        if mutuelle is not None:
            job_detail.mutuelle = mutuelle

        # If grade or echelon changed, recalculate indice
        if grade is not None or echelon is not None:
            new_grade = grade if grade is not None else job_detail.grade
            new_echelon = echelon if echelon is not None else job_detail.echelon

            job_detail.grade = new_grade
            job_detail.echelon = new_echelon
            job_detail.indice = JobDetailService.calculate_indice(
                new_grade, new_echelon
            )

        job_detail.save()
        return job_detail
