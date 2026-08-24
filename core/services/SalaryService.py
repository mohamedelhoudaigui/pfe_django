from typing import Tuple, Dict
from decimal import Decimal, ROUND_HALF_UP
from ..models import CivilServant, JobDetail, SalaryDetail
from .JobDetailService import JobDetailService
from .GradeIndemnitiesService import GradeIndemnitiesService
from django.shortcuts import get_object_or_404


class SalaryService:

    ZONE_RATE = {"A": Decimal("0.25"), "B": Decimal("0.15"), "C": Decimal("0.10")}
    TAX_BRACKETS = [
        (Decimal("0"), Decimal("40000"), Decimal("0"), Decimal("0")),
        (Decimal("40001"), Decimal("60000"), Decimal("0.10"), Decimal("4000")),
        (Decimal("60001"), Decimal("80000"), Decimal("0.20"), Decimal("10000")),
        (Decimal("80001"), Decimal("100000"), Decimal("0.30"), Decimal("18000")),
        (Decimal("100001"), Decimal("180000"), Decimal("0.34"), Decimal("22000")),
        (Decimal("180001"), Decimal("Infinity"), Decimal("0.37"), Decimal("27400")),
    ]
    BASE_CONST_1 = Decimal("50.92")
    BASE_CONST_2 = Decimal("6228")
    FRACTIONAL_POINTS = Decimal("0.01")

    @staticmethod
    def _q(value) -> Decimal:
        """Round a value to 2 decimal places (money precision)."""
        return Decimal(value).quantize(
            SalaryService.FRACTIONAL_POINTS, rounding=ROUND_HALF_UP
        )

    @staticmethod
    def get_base_salary(job_detail: JobDetail) -> Decimal:
        return SalaryService._q(
            job_detail.indice * SalaryService.BASE_CONST_1 + SalaryService.BASE_CONST_2
        )

    @staticmethod
    def get_indemnities(
        job_detail: JobDetail, TB
    ) -> Dict[str, Decimal]:
        zone_indemnity = SalaryService._q(TB * SalaryService.ZONE_RATE[job_detail.zone])
        indemnities = GradeIndemnitiesService.get_indemnities(job_detail)
        indemnities["zone"] = zone_indemnity
        return indemnities

    @staticmethod
    def get_TSP(TB, indemnities) -> Decimal:
        return SalaryService._q(TB + sum(indemnities.values()))

    @staticmethod
    def get_AF(n_enfants) -> Decimal:
        if n_enfants <= 3:
            AF = Decimal(n_enfants) * Decimal("300")
        elif n_enfants <= 6:
            AF = Decimal("3") * Decimal("300") + (
                Decimal(n_enfants) - Decimal("3")
            ) * Decimal("100")
        else:
            AF = Decimal("3") * Decimal("300") + Decimal("3") * Decimal("100")
            # yearly value
        return SalaryService._q(AF * 12)

    @staticmethod
    def get_monthly_deductions(
        TSP: Decimal, echelle: str
    ) -> Tuple[Decimal, Decimal, Decimal, Decimal, Decimal]:
        CMR = SalaryService._q(TSP * Decimal("0.14") / Decimal(12))
        AMO = max(
            Decimal("70"),
            min(
                Decimal("400"), SalaryService._q(TSP * Decimal("0.025") / Decimal("12"))
            ),
        )
        SM = min(
            Decimal("80"), SalaryService._q(TSP * Decimal("0.015") / Decimal("12"))
        )
        CCD = min(
            Decimal("100"), SalaryService._q(TSP * Decimal("0.01") / Decimal("12"))
        )
        FOS = 0
        # hydrogen bomb here (handle later):
        if int(echelle) <= 6:
            FOS = SalaryService._q("25")
        if int(echelle) <= 10:
            FOS = SalaryService._q("50")
        if int(echelle) <= 11:
            FOS = SalaryService._q("80")
        elif int(echelle) > 11:
            FOS = SalaryService._q("120")
        return (CMR, AMO, SM, CCD, FOS)

    @staticmethod
    def get_income_reduction(TSP: Decimal) -> Decimal:
        if TSP <= Decimal("78000"):
            result = min(Decimal("35000"), TSP * Decimal("0.35"))
        else:
            result = min(Decimal("35000"), TSP * Decimal("0.25"))
        return SalaryService._q(result)

    @staticmethod
    def get_taxable_income(
        TSP: Decimal,
        monthly_deductions: Tuple[Decimal, Decimal, Decimal, Decimal, Decimal],
    ) -> Decimal:
        CMR, AMO, SM, CCD, FOS = monthly_deductions
        return SalaryService._q(
            TSP
            - SalaryService.get_income_reduction(TSP)
            - (CMR + AMO + SM + CCD + FOS) * 12
        )

    @staticmethod
    def get_income_tax(
        TSP: Decimal,
        monthly_deductions: Tuple[Decimal, Decimal, Decimal, Decimal, Decimal],
        n_enfants: int,
        is_married: Decimal,
    ) -> Decimal:
        taxable_income = SalaryService.get_taxable_income(TSP, monthly_deductions)
        taxable_amount = Decimal("0")
        for group in SalaryService.TAX_BRACKETS:
            if taxable_income >= group[0] and taxable_income <= group[1]:
                taxable_amount = taxable_income * group[2] - group[3]
                break
        family_reduction = min(Decimal(6), Decimal(n_enfants) + is_married) * Decimal(
            "600"
        )
        return max(Decimal("0"), taxable_amount - family_reduction)

    @staticmethod
    def save_to_model(
        civil_servant: CivilServant, job_detail: JobDetail
    ) -> SalaryDetail:
        """
        Calculate and persist the SalaryDetail for a civil servant.

        Args:
            civil_servant: CivilServant instance
            job_detail: JobDetail instance (optional — fetched automatically if not provided)

        Returns:
            Created or updated SalaryDetail instance
        """
        if job_detail is None:
            job_detail = JobDetailService.get_jobdetail(civil_servant)

        n_enfants = civil_servant.n_enfants
        echelle = job_detail.echelle
        is_married = (
            Decimal("1")
            if civil_servant.situation_familiale == "married"
            else Decimal("0")
        )

        TB = SalaryService.get_base_salary(job_detail)
        indemnities = SalaryService.get_indemnities(job_detail, TB)
        TSP = SalaryService.get_TSP(TB, indemnities)
        AF = SalaryService.get_AF(n_enfants)

        TEA = TSP + AF
        TEM = TEA / Decimal("12")

        monthly_deductions = SalaryService.get_monthly_deductions(TSP, echelle)
        CMR, AMO, SM, CCD, FOS = monthly_deductions
        IR = SalaryService.get_income_tax(
            TSP, monthly_deductions, n_enfants, is_married
        )

        net_salary = SalaryService._q(TEM - CMR - AMO - SM - CCD - FOS - IR)

        salary_detail, _ = SalaryDetail.objects.update_or_create(
            civil_servant=civil_servant,
            defaults={
                "base_salary": TB,
                "indemnities": indemnities,
                "tsp": TSP,
                "family_allowance": AF,
                "annual_gross_salary": TEA,
                "monthly_gross_salary": TEM,
                "cmr": CMR,
                "amo": AMO,
                "sm": SM,
                "ccd": CCD,
                "fos": FOS,
                "income_reduction": SalaryService.get_income_reduction(TSP),
                "taxable_income": SalaryService.get_taxable_income(
                    TSP, monthly_deductions
                ),
                "income_tax": IR,
                "net_salary": net_salary,
            },
        )

        return salary_detail

    @staticmethod
    def get_salary_with_id(id: int) -> SalaryDetail:
        return get_object_or_404(SalaryDetail, civil_servant__id=id)

    @staticmethod
    def get_salary_with_CIN(CIN: str) -> SalaryDetail:
        return get_object_or_404(SalaryDetail, civil_servant__CIN=CIN)
