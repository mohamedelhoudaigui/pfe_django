from ..models import CivilServant, JobDetail, EchelonIndice, Grade, Categorie
from django.shortcuts import get_object_or_404


class JobDetailService:
    """Service for managing job detail business logic."""

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
            categorie: The categorie code of the civil servant (e.g. 'technicien', ...)
            grade: The grade code (e.g., '4G', '3G', '2G', '1G')
            echelon: The echelon level (1-13)

        Returns:
            The calculated indice value

        Raises:
            ValueError: If categorie, grade or echelon is invalid
        """
        try:
            echelon_indice = EchelonIndice.objects.select_related("grade__categorie").get(
                grade__categorie__code=categorie,
                grade__code=grade,
                echelon=echelon,
            )
        except EchelonIndice.DoesNotExist:
            # figure out which part is invalid, to keep the same error granularity
            if not Categorie.objects.filter(code=categorie).exists():
                raise ValueError(f"Invalid categorie: {categorie}")
            if not Grade.objects.filter(categorie__code=categorie, code=grade).exists():
                raise ValueError(f"Invalid grade {grade} for categorie {categorie}")
            raise ValueError(f"Invalid echelon {echelon} for grade {grade}")

        return echelon_indice.indice

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
