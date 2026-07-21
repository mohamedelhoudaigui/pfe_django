from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

# Create your models here.


class CivilServant(models.Model):

    GENRE_CHOICES = [
        ("man", "man"),
        ("woman", "woman"),
    ]

    SITUATION_FAMILIALE_CHOICES = [
        ("single", "single"),
        ("married", "married"),
        ("divorced", "married"),
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
    CATEGORIES = [("technicien", "technicien")]
    GRADES = [("1G", "1G"), ("2G", "2G"), ("3G", "3G"), ("4G", "4G")]
    # Echelle no 12 = Hors echelle
    ECHELLE = [(i, str(i)) for i in range(1, 13)]
    ECHELON = [(i, str(i)) for i in range(1, 14)]
    MUTUELLE = [("CNOPS", "CNOPS")]

    civil_servant = models.OneToOneField(
        "CivilServant", on_delete=models.CASCADE, related_name="JobDetail"
    )

    zone = models.CharField(max_length=1, choices=ZONES)
    categorie = models.CharField(max_length=100, choices=CATEGORIES)
    grade = models.CharField(max_length=10, choices=GRADES)
    echelle = models.PositiveSmallIntegerField(choices=ECHELLE)
    echelon = models.PositiveSmallIntegerField(choices=ECHELON)
    indice = models.PositiveSmallIntegerField(editable=False)
    mutuelle = models.CharField(max_length=50, choices=MUTUELLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.civil_servant} — {self.grade} / Echelon {self.echelon} / Indice {self.indice}"

    @property
    def exceptionelle(self):
        """درجة استثنائية only exists in 2G rank 11"""
        return self.grade == "2G" and self.echelon == 11

    @property
    def hors_echelle(self):
        return self.echelle > 11


class SalaryDetail(models.Model):
    civil_servant = models.OneToOneField(
        "CivilServant", on_delete=models.CASCADE, related_name="SalaryDetail"
    )
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    indemnities = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
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
    fos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    income_reduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salary detail for {self.civil_servant}"
