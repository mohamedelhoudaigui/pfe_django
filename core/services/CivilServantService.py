from django.db import transaction
from ..models import CivilServant, JobDetail, SalaryDetail
from .JobDetailService import JobDetailService
from .SalaryService import SalaryService
from django.shortcuts import get_object_or_404


class CivilServantService:
    """Service for managing civil servant business logic and orchestration."""

    @staticmethod
    @transaction.atomic
    def create_civil_servant_with_job_and_salary(
        civil_servant_data: dict, job_detail_data: dict
    ) -> CivilServant:
        """
        Create a civil servant with optional job detail and salary detail.

        This method orchestrates the creation of a CivilServant along with related
        JobDetail and SalaryDetail records in a single atomic transaction.

        Args:
            civil_servant_data: Dictionary with CivilServant fields
                (CIN, PPR, nom, prenom, date_de_naissance, lieu_de_naissance,
                 genre, situation_familiale, n_enfants, address)
            job_detail_data: Optional dictionary with JobDetail fields
                (zone, categorie, grade, echelon, mutuelle)

        Returns:
            Created CivilServant instance with related objects

        Raises:
            ValueError: If validation fails
            IntegrityError: If unique constraints are violated
        """
        # Create the civil servant
        civil_servant = CivilServant.objects.create(**civil_servant_data)

        # If job detail data is provided, create job detail and salary
        JobDetailService.create_job_detail(civil_servant, job_detail_data)

        SalaryService(civil_servant).save_to_model()

        return civil_servant

    @staticmethod
    def get_civil_servant_with_id(id: int) -> CivilServant:
        return get_object_or_404(CivilServant, id=id)

    @staticmethod
    def get_civil_servant_with_CIN(CIN: str) -> CivilServant:
        return get_object_or_404(CivilServant, CIN=CIN)

    @staticmethod
    def get_all_civil_servants() -> list:
        return CivilServant.objects.all()

    @staticmethod
    @transaction.atomic
    def update_civil_servant(
        civil_servant_id: int,
        civil_servant_updates: dict = None,
        job_detail_updates: dict = None,
    ) -> CivilServant:

        civil_servant = CivilServant.objects.get(id=civil_servant_id)
        job_detail = civil_servant.JobDetail

        if civil_servant_updates:
            for key, value in civil_servant_updates.items():
                setattr(civil_servant, key, value)
            civil_servant.save()

        if job_detail_updates:
            JobDetailService.update_job_detail(job_detail, **job_detail_updates)

        salary_service = SalaryService(civil_servant)
        salary_service.save_to_model()

        return (
            CivilServant.objects.select_related("JobDetail")
            .prefetch_related("salary_details")
            .get(id=civil_servant_id)
        )

    @staticmethod
    @transaction.atomic
    def delete_civil_servant(civil_servant_id: int) -> None:
        """
        Delete a civil servant and all related records.

        Args:
            civil_servant_id: ID of the civil servant to delete

        Raises:
            CivilServant.DoesNotExist: If civil servant not found
        """
        civil_servant = CivilServant.objects.get(id=civil_servant_id)
        civil_servant.delete()

    @staticmethod
    def get_civil_servants_by_grade(grade: str) -> list:
        """
        Retrieve all civil servants with a specific grade.

        Args:
            grade: Grade code to filter by

        Returns:
            QuerySet of CivilServant instances with the specified grade
        """
        return (
            CivilServant.objects.filter(JobDetail__grade=grade)
            .select_related("JobDetail")
            .prefetch_related("salary_details")
        )

    @staticmethod
    def get_civil_servants_by_zone(zone: str) -> list:
        """
        Retrieve all civil servants assigned to a specific zone.

        Args:
            zone: Zone code to filter by

        Returns:
            QuerySet of CivilServant instances in the specified zone
        """
        return (
            CivilServant.objects.filter(JobDetail__zone=zone)
            .select_related("JobDetail")
            .prefetch_related("salary_details")
        )
