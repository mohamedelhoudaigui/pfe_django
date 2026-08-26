from decimal import Decimal, ROUND_HALF_UP
from django.test import TestCase
from core.services.SalaryService import SalaryService
from core.services.CivilServantService import CivilServantService
from core.services.JobDetailService import JobDetailService
from core.services.SeedService import SeedService


class SalaryDetailServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Seed Categorie/Grade/EchelonIndice reference data into the test DB.
        Test DBs are created fresh and empty each run, so calculate_indice()
        has nothing to look up unless we seed it here first.
        """
        SeedService.seed_categorie_grade_indice(force=True)

    def _q(self, value) -> Decimal:
        """Round a value to 2 decimal places (money precision)."""
        return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def test_salary_service_calculation_steps_for_zone_c_3g_echelon_9(self):
        civil_servant = CivilServantService.create_civil_servant(
            civil_servant_data={
                "CIN": "AA1257",
                "PPR": "PPR02",
                "nom": "Jack",
                "prenom": "Test",
                "date_de_naissance": "1985-05-05",
                "lieu_de_naissance": "Rabat",
                "genre": "man",
                "situation_familiale": "married",
                "n_enfants": 1,
                "address": "Rue Exemple 1",
            },
            job_detail_data={
                "zone": "C",
                "categorie": "technicien",
                "grade": "3G",
                "echelle": "9",
                "echelon": 9,
                "mutuelle": "CNOPS",
            },
            login_data={
                "username": "test1",
                "password": "test1test2",
                "email": "test@test.com",
            },
        )

        job_detail = JobDetailService.get_jobdetail(civil_servant=civil_servant)

        base_salary = SalaryService.get_base_salary(job_detail)
        indemnities = SalaryService.get_indemnities(job_detail, base_salary)
        tsp = SalaryService.get_TSP(base_salary, indemnities)
        family_allowance = SalaryService.get_AF(civil_servant.n_enfants)
        annual_gross_salary = self._q(tsp + family_allowance)  # TEA
        monthly_gross_salary = self._q(annual_gross_salary / Decimal("12"))  # TEM
        cmr, amo, sm, ccd, fos = SalaryService.get_monthly_deductions(
            tsp, job_detail.echelle
        )
        income_reduction = SalaryService.get_income_reduction(tsp)
        taxable_income = SalaryService.get_taxable_income(tsp, (cmr, amo, sm, ccd, fos))
        income_tax = SalaryService.get_income_tax(
            tsp, (cmr, amo, sm, ccd, fos), civil_servant.n_enfants, Decimal(1)
        )
        net_salary = (
            monthly_gross_salary - cmr - amo - sm - ccd - fos - income_tax
        ).quantize(Decimal("0.01"))

        print("--- Salary calculation steps ---")
        print(f"indice: {job_detail.indice}")
        print(f"base_salary: {base_salary}")

        print(f"indemnities:")
        for key, value in indemnities.items():
            print(f"    {key} indemnity: {value}")

        print(f"tsp: {tsp}")
        print(f"family_allowance: {family_allowance}")
        print(f"annual_gross_salary: {annual_gross_salary}")
        print(f"monthly_gross_salary: {monthly_gross_salary}")
        print(f"cmr: {cmr}")
        print(f"amo: {amo}")
        print(f"sm: {sm}")
        print(f"ccd: {ccd}")
        print(f"fos: {fos}")
        print(f"income_tax(IR): {income_tax}")
        print(f"net_salary: {net_salary}")

        # testing equality
        self.assertEqual(job_detail.indice, 404)
        self.assertEqual(base_salary, Decimal("26799.68"))

        # check indemnities
        self.assertEqual(indemnities["zone"], Decimal("2679.97"))
        self.assertEqual(indemnities["technicality"], Decimal("55620.00"))
        self.assertEqual(indemnities["burdens"], Decimal("3660.00"))

        # TSP /TEA / TEM
        self.assertEqual(tsp, Decimal("88759.65"))
        self.assertEqual(annual_gross_salary, Decimal("92359.65"))
        self.assertEqual(monthly_gross_salary, Decimal("7696.64"))

        # family allowances
        self.assertEqual(family_allowance, Decimal("3600.00"))

        # check deductions
        self.assertEqual(cmr, Decimal("1035.53"))
        self.assertEqual(amo, Decimal("184.92"))
        self.assertEqual(sm, Decimal("80.00"))
        self.assertEqual(ccd, Decimal("73.97"))
        self.assertEqual(income_tax, Decimal("0"))
        self.assertEqual(net_salary, Decimal("6242.22"))