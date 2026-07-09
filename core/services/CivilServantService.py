from django.db import transaction
from ..models import CivilServant, JobDetail, SalaryDetail
from .JobDetailService import JobDetailService
from .SalaryService import SalaryService


class CivilServantService:
    """Service for managing civil servant business logic and orchestration."""

    @staticmethod
    @transaction.atomic
    def create_civil_servant_with_job_and_salary(
        civil_servant_data: dict, job_detail_data: dict = None
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
        if job_detail_data:
            JobDetailService.create_job_detail(
                civil_servant=civil_servant,
                zone=job_detail_data["zone"],
                categorie=job_detail_data["categorie"],
                grade=job_detail_data["grade"],
                echelle=job_detail_data["echelle"],
                echelon=job_detail_data["echelon"],
                mutuelle=job_detail_data["mutuelle"],
            )

            # Create salary detail based on job detail
            SalaryService(civil_servant).save_to_model()

        return civil_servant

    @staticmethod
    def get_civil_servant_with_related(civil_servant_id: int) -> CivilServant:
        """
        Retrieve a civil servant with all related objects (optimized query).

        Args:
            civil_servant_id: ID of the civil servant

        Returns:
            CivilServant instance with prefetched related objects

        Raises:
            CivilServant.DoesNotExist: If civil servant not found
        """
        return (
            CivilServant.objects.select_related("JobDetail")
            .prefetch_related("salary_details")
            .get(id=civil_servant_id)
        )

    @staticmethod
    def get_all_civil_servants() -> list:
        """
        Retrieve all civil servants with optimized queries.

        Returns:
            QuerySet of CivilServant instances with prefetched related objects
        """
        return CivilServant.objects.select_related("JobDetail").prefetch_related(
            "salary_details"
        )

    @staticmethod
    @transaction.atomic
    def update_civil_servant(
        civil_servant_id: int,
        civil_servant_updates: dict = None,
        job_detail_updates: dict = None,
        recalculate_salary: bool = False,
    ) -> CivilServant:
        """
        Update a civil servant and optionally its job detail and salary.

        If salary recalculation is needed (e.g., due to grade change), this method
        will automatically recalculate and update the salary detail.

        Args:
            civil_servant_id: ID of the civil servant to update
            civil_servant_updates: Dictionary with CivilServant field updates
            job_detail_updates: Dictionary with JobDetail field updates
            recalculate_salary: Whether to recalculate salary after updates

        Returns:
            Updated CivilServant instance

        Raises:
            CivilServant.DoesNotExist: If civil servant not found
            ValueError: If validation fails
        """
        civil_servant = CivilServant.objects.get(id=civil_servant_id)

        # Update civil servant fields
        if civil_servant_updates:
            for key, value in civil_servant_updates.items():
                setattr(civil_servant, key, value)
            civil_servant.save()

        # Update job detail if provided
        if job_detail_updates:
            try:
                job_detail = civil_servant.JobDetail
                JobDetailService.update_job_detail(job_detail, **job_detail_updates)
                recalculate_salary = True  # Grade/echelon changes require salary recalc
            except JobDetail.DoesNotExist:
                # Create job detail if it doesn't exist
                JobDetailService.create_job_detail(
                    civil_servant=civil_servant, **job_detail_updates
                )
                recalculate_salary = True

        # Recalculate salary if needed
        if recalculate_salary:
            try:
                job_detail = civil_servant.JobDetail
                salary_service = SalaryService(civil_servant, job_detail)
                salary_service.save_to_model()
            except JobDetail.DoesNotExist:
                pass  # No job detail, skip salary calculation

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
