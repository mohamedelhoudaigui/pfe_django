from typing import Tuple, Dict
from decimal import Decimal, ROUND_HALF_UP
from ..models import CivilServant, SalaryDetail
from .JobDetailService import JobDetailService
from .GradeIndemnitiesService import GradeIndemnitiesService


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

    def __init__(self, civil_servant: CivilServant):
        self.civil_servant = civil_servant
        self.job_detail = JobDetailService.get_jobdetail(civil_servant)
        self.grade_indemnities = GradeIndemnitiesService(civil_servant)

    @staticmethod
    def _q(value) -> Decimal:
        """Round a value to 2 decimal places (money precision)."""
        return Decimal(value).quantize(
            SalaryService.FRACTIONAL_POINTS, rounding=ROUND_HALF_UP
        )

    def get_base_salary(self) -> Decimal:
        return self._q(self.job_detail.indice * self.BASE_CONST_1 + self.BASE_CONST_2)

    def get_indemnities(self, TB) -> Dict[str, Decimal]:
        zone_indemnity = self._q(TB * self.ZONE_RATE[self.job_detail.zone])
        indemnities = self.grade_indemnities.get_indemnities()
        indemnities["zone"] = zone_indemnity
        return indemnities

    def get_TSP(self, TB, indemnities) -> Decimal:
        return self._q(TB + sum(indemnities.values()))

    def get_AF(self, n_enfants) -> Decimal:
        if n_enfants <= 3:
            AF = Decimal(n_enfants) * Decimal("300")
        elif n_enfants <= 6:
            AF = Decimal("3") * Decimal("300") + (
                Decimal(n_enfants) - Decimal("3")
            ) * Decimal("100")
        else:
            AF = Decimal("3") * Decimal("300") + Decimal("3") * Decimal("100")
            # yearly value
        return self._q(AF * 12)

    def get_monthly_deductions(
        self, TSP: Decimal, echelle: str
    ) -> Tuple[Decimal, Decimal, Decimal, Decimal, Decimal]:
        CMR = self._q(TSP * Decimal("0.14") / Decimal(12))
        AMO = max(
            Decimal("70"),
            min(Decimal("400"), self._q(TSP * Decimal("0.025") / Decimal("12"))),
        )
        SM = min(Decimal("80"), self._q(TSP * Decimal("0.015") / Decimal("12")))
        CCD = min(Decimal("100"), self._q(TSP * Decimal("0.01") / Decimal("12")))
        FOS = 0
        if echelle <= 6:
            FOS = self._q("25")
        if echelle <= 10:
            FOS = self._q("50")
        if echelle <= 11:
            FOS = self._q("80")
        elif echelle > 11:
            FOS = self._q("120")
        return (CMR, AMO, SM, CCD, FOS)

    def get_income_reduction(self, TSP: Decimal) -> Decimal:
        if TSP <= Decimal("78000"):
            result = min(Decimal("35000"), TSP * Decimal("0.35"))
        else:
            result = min(Decimal("35000"), TSP * Decimal("0.25"))
        return self._q(result)

    def get_taxable_income(
        self,
        TSP: Decimal,
        monthly_deductions: Tuple[Decimal, Decimal, Decimal, Decimal, Decimal],
    ) -> Decimal:
        CMR, AMO, SM, CCD, FOS = monthly_deductions
        return self._q(
            TSP - self.get_income_reduction(TSP) - (CMR + AMO + SM + CCD + FOS) * 12
        )

    def get_income_tax(
        self,
        TSP: Decimal,
        monthly_deductions: Tuple[Decimal, Decimal, Decimal, Decimal, Decimal],
        n_enfants: int,
        is_married: Decimal,
    ) -> Decimal:
        taxable_income = self.get_taxable_income(TSP, monthly_deductions)
        taxable_amount = Decimal("0")
        for group in self.TAX_BRACKETS:
            if taxable_income >= group[0] and taxable_income <= group[1]:
                taxable_amount = taxable_income * group[2] - group[3]
                break
        family_reduction = min(Decimal(6), Decimal(n_enfants) + is_married) * Decimal(
            "600"
        )
        return max(Decimal("0"), taxable_amount - family_reduction)

    def save_to_model(self) -> SalaryDetail:
        n_enfants = self.civil_servant.n_enfants
        echelle = self.job_detail.echelle
        is_married = (
            Decimal("1")
            if self.civil_servant.situation_familiale == "married"
            else Decimal("0")
        )

        TB = self.get_base_salary()
        indemnities = self.get_indemnities(TB)
        TSP = self.get_TSP(TB, indemnities)
        AF = self.get_AF(n_enfants)

        TEA = TSP + AF
        TEM = TEA / Decimal("12")

        monthly_deductions = self.get_monthly_deductions(TSP, echelle)
        CMR, AMO, SM, CCD, FOS = monthly_deductions
        IR = self.get_income_tax(TSP, monthly_deductions, n_enfants, is_married)

        net_salary = self._q(TEM - CMR - AMO - SM - CCD - FOS - IR)

        salary_detail = SalaryDetail.objects.create(
            civil_servant=self.civil_servant,
            base_salary=TB,
            indemnities=indemnities,
            tsp=TSP,
            family_allowance=AF,
            annual_gross_salary=TEA,
            monthly_gross_salary=TEM,
            cmr=CMR,
            amo=AMO,
            sm=SM,
            ccd=CCD,
            fos=FOS,
            income_reduction=self.get_income_reduction(TSP),
            taxable_income=self.get_taxable_income(TSP, monthly_deductions),
            income_tax=IR,
            net_salary=net_salary,
        )

        return salary_detail
