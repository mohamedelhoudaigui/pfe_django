from django.db import models

# Create your models here.


class CivilServant(models.Model):

    GENRE_CHOICES = [
        ("man", "Homme"),
        ("woman", "Femme"),
    ]

    SITUATION_FAMILIALE_CHOICES = [
        ("single", "Célibataire"),
        ("married", "Marié(e)"),
        ("divorced", "Divorcé(e)"),
    ]

    CIN = models.CharField(max_length=20, unique=True)
    PPR = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    lieu_de_naissance = models.CharField(max_length=100)
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES)
    situation_familiale = models.CharField(
        max_length=20, choices=SITUATION_FAMILIALE_CHOICES
    )
    n_enfants = models.PositiveIntegerField(default=0)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class JobDetail(models.Model):

    ZONES = [("A", "A"), ("B", "B"), ("C", "C")]

    CATEGORIES = [("technicien", "Techniciens")]

    GRADES = [("1G", "1G"), ("2G", "2G"), ("3G", "3G"), ("4G", "4G")]

    ECHELLON = [(i, str(i)) for i in range(1, 14)]

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

    MUTUELLE = [("CNOPS", "CNOPS")]

    fonct = models.OneToOneField(
        "CivilServant", on_delete=models.CASCADE, related_name="JobDetail"
    )
    zone = models.CharField(max_length=1, choices=ZONES)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    grade = models.CharField(max_length=10, choices=GRADES)
    echelon = models.PositiveSmallIntegerField(choices=ECHELLON)
    indice = models.PositiveSmallIntegerField(editable=False)
    mutuelle = models.CharField(max_length=50, choices=MUTUELLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fonct} — {self.grade} / Echelon {self.echelon} / Indice {self.index}"

    def save(self, *args, **kwargs):
        grade_table = self.ECHELON_INDICE_TABLEAU.get(
            self.grade, {}
        )  # default empty dic
        self.indice = grade_table.get(self.echelon, 0)
        super().save(*args, **kwargs)

    @property
    def is_exceptional(self):
        """درجة استثنائية only exists in 2G rank 11"""
        return self.grade == "2G" and self.echelon == 11


class SalaryDetail(models.Model):
    civil_servant = models.ForeignKey(
        CivilServant,
        on_delete=models.CASCADE,
        related_name="salary_details",
    )
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    zone_indemnity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tsp = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    family_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    annual_gross_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    monthly_gross_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    cmr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ccd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    income_reduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salary detail for {self.civil_servant}"
