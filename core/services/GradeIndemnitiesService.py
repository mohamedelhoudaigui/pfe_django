from decimal import Decimal, ROUND_HALF_UP
from ..models import CivilServant
from .JobDetailService import JobDetailService
from typing import Dict

# indemnities are gonna be provided as dictionaries in the following form:
# {
#   "INDEMNITIE_NAME": INDEMNITIE VALUE (DECIMAL)
#   ...
# }
#
# types of indemnities are :
# special_administrative
# burdens
# mentoring
# technicality
# administratif_progression




class GradeIndemnitiesService:
    def __init__(self, civil_servant: CivilServant):
        self.civil_servant = civil_servant
        self.job_detail = JobDetailService.get_jobdetail(self.civil_servant)

    @staticmethod
    def _q(value) -> Decimal:
        """Round a value to 2 decimal places (money precision)."""
        return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_indemnities(self) -> Dict[str, Decimal]:
        categorie = self.job_detail.categorie
        grade = self.job_detail.grade
        step = self.job_detail.echelon

        # we multiply the indemnities X 12 to get yearly value of them

        indemnities = {}
        if categorie == "technicien":
            if grade == "4G":
                indemnities["technicality"] = 4420
                indemnities["burdens"] = 305

            elif grade == "3G":
                indemnities["technicality"] = 4635
                indemnities["burdens"] = 305

            elif grade == "2G":
                if step <= 5:
                    indemnities["technicality"] = 5055
                else:
                    indemnities["technicality"] = 5182
                    indemnities["mentoring"] = 700
                indemnities["burdens"] = 1000

            elif grade == "1G":
                if step <= 5:
                    indemnities["technicality"] = 6638
                    indemnities["mentoring"] = 950
                elif step <= 10:
                    indemnities["technicality"] = 8171
                    indemnities["mentoring"] = 3600
                elif step <= 13:
                    indemnities["technicality"] = 8594
                    indemnities["mentoring"] = 3600
                indemnities["burdens"] = 1000

        for key in indemnities:
            indemnities[key] = self._q(indemnities[key] * 12)

        return indemnities
