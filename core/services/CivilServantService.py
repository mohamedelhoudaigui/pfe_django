from django.db import transaction, IntegrityError
from ..models import CivilServant
from .JobDetailService import JobDetailService
from .SalaryService import SalaryService
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class CivilServantService:
    """Service for managing civil servant business logic and orchestration."""

    @staticmethod
    @transaction.atomic
    def create_civil_servant(
        civil_servant_data: dict,
        job_detail_data: dict,
        login_data: dict,
    ) -> CivilServant:
        """
        Create a civil servant with job detail, salary detail and login.

        This method orchestrates the creation of a CivilServant along with related
        JobDetail, SalaryDetail and User records in a single atomic transaction.

        Args:
            civil_servant_data: Dictionary with CivilServant fields
                (CIN, PPR, nom, prenom, date_de_naissance, lieu_de_naissance,
                 genre, situation_familiale, n_enfants, address)
            job_detail_data: dictionary with JobDetail fields
                (zone, categorie, grade, echelon, mutuelle)
            login_data: dictionary with login informations
                (username, password, email)

        Returns:
            Created CivilServant instance with related objects

        Raises:
            ValueError: If validation fails
            IntegrityError: If unique constraints are violated
        """
        # check duplicated email
        email = login_data.get("email")

        if email and User.objects.filter(email__iexact=email).exists():
            raise IntegrityError(f"A user with email '{email}' already exists.")

        # Create the civil servant
        user = User.objects.create_user(**login_data)
        civil_servant = CivilServant.objects.create(user=user, **civil_servant_data)

        # If job detail data is provided, create job detail and salary
        job_detail = JobDetailService.save_job_detail(civil_servant, job_detail_data)

        SalaryService.save_to_model(civil_servant, job_detail)

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
            JobDetailService.save_job_detail(civil_servant, job_detail_updates)

        salary_service = SalaryService(civil_servant)
        salary_service.save_to_model()

        return CivilServant.objects.get(id=civil_servant_id)

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
