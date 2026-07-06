from decimal import Decimal, ROUND_HALF_UP
from django.test import TestCase
from core.services.SalaryService import SalaryService
from core.services.CivilServantService import CivilServantService
from core.services.JobDetailService import JobDetailService

# class CivilServantSerializerTest(TestCase):
#     def test_serializer_creates_job_and_salary_details(self):
#         payload = {
#             "CIN": "AA123456",
#             "PPR": "PPR001",
#             "nom": "Test",
#             "prenom": "User",
#             "date_de_naissance": "1990-01-01",
#             "lieu_de_naissance": "Rabat",
#             "genre": "man",
#             "situation_familiale": "single",
#             "n_enfants": 0,
#             "address": "123 Main St",
#             "job_detail": {
#                 "zone": "A",
#                 "category": "technicien",
#                 "grade": "1G",
#                 "echelon": 1,
#                 "mutuelle": "CNOPS",
#             },
#         }

#         serializer = CivilServantSerializer(data=payload)
#         self.assertTrue(serializer.is_valid(), serializer.errors)

#         civil_servant = serializer.save()

#         self.assertTrue(JobDetail.objects.filter(fonct=civil_servant).exists())
#         self.assertTrue(
#             SalaryDetail.objects.filter(civil_servant=civil_servant).exists()
#         )


class SalaryDetailServiceTest(TestCase):

    # in storing try to see if we store the values monthly or annually
    # some of our values are monthly and some the other way we should seek one or the another

    def _q(self, value) -> Decimal:
        """Round a value to 2 decimal places (money precision)."""
        return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def test_salary_service_calculation_steps_for_zone_c_3g_echelon_9(self):
        civil_servant = CivilServantService.create_civil_servant_with_job_and_salary(
            {
                "CIN": "AA123457",
                "PPR": "PPR002",
                "nom": "Jack",
                "prenom": "Test",
                "date_de_naissance": "1985-05-05",
                "lieu_de_naissance": "Rabat",
                "genre": "man",
                "situation_familiale": "married",
                "n_enfants": 1,
                "address": "Rue Exemple 1",
            },
            {
                "zone": "C",
                "category": "technicien",
                "grade": "3G",
                "echelon": 9,
                "mutuelle": "CNOPS",
            },
        )

        job_detail = JobDetailService.get_jobdetail(civil_servant)
        service = SalaryService(civil_servant)

        base_salary = service.get_base_salary()
        indemnities = service.get_indemnities(base_salary)
        tsp = service.get_TSP(base_salary, indemnities)
        family_allowance = service.get_AF(civil_servant.n_enfants)
        annual_gross_salary = self._q(tsp + family_allowance)  # TEA
        monthly_gross_salary = self._q(annual_gross_salary / Decimal("12"))  # TEM
        cmr, amo, sm, ccd = service.get_monthly_deductions(tsp)
        income_reduction = service.get_income_reduction(tsp)
        taxable_income = service.get_taxable_income(tsp, (cmr, amo, sm, ccd))
        income_tax = service.get_income_tax(
            tsp, (cmr, amo, sm, ccd), civil_servant.n_enfants, Decimal(1)
        )
        net_salary = (
            monthly_gross_salary - cmr - amo - sm - ccd - income_tax
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
        print(f"income_reduction: {income_reduction}")
        print(f"taxable_income: {taxable_income}")
        print(f"income_tax: {income_tax}")
        print(f"net_salary: {net_salary}")

        # self.assertEqual(job_detail.indice, 404)
        # self.assertEqual(base_salary, Decimal("26799.68"))
        # # check indemnities
        # self.assertEqual(tsp, Decimal("29479.65"))
        # self.assertEqual(family_allowance, Decimal("300.00"))
        # self.assertEqual(annual_gross_salary, Decimal("29779.65"))
        # self.assertEqual(monthly_gross_salary, Decimal("2481.64"))
        # self.assertEqual(cmr, Decimal("343.93"))
        # self.assertEqual(amo, Decimal("70.00"))
        # self.assertEqual(sm, Decimal("36.85"))
        # self.assertEqual(ccd, Decimal("24.57"))
        # self.assertEqual(income_reduction, Decimal("10317.88"))
        # self.assertEqual(taxable_income, Decimal("13457.57"))
        # self.assertEqual(income_tax, Decimal("0"))
        # self.assertEqual(net_salary, Decimal("2006.29"))
