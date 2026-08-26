from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

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

    # this field gives the ablitiy of authorization to the civil servant model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="civil_servant"
    )
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
    MUTUELLE = [("CNOPS", "CNOPS")]

    POSITIONS = [
        ("en_activite", "En activité"),
        ("abandon_de_poste", "Abandon de poste"),
        ("conge_de_maladie", "Congé de maladie"),
        ("decharge_syndicale", "Décharge syndicale"),
        ("demission", "Démission"),
        ("detachement", "Détachement"),
        ("licenciement", "Licenciement"),
        ("mise_a_disposition", "Mise à disposition"),
        ("mise_en_disponibilite", "Mise en disponibilité"),
        ("mutation", "Mutation"),
        ("position_militaire", "Position militaire"),
        ("stagiaire", "Stagiaire"),
        ("suspension_provisoire", "Suspension provisoire"),
    ]

    civil_servant = models.OneToOneField(
        "CivilServant", on_delete=models.CASCADE, related_name="JobDetail"
    )

    zone = models.CharField(max_length=1, choices=ZONES)
    categorie = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    echelle = models.CharField(max_length=10, help_text="Associated with grade, e.g. tech 4th grade = échelle 9")
    echelon = models.PositiveSmallIntegerField(help_text="1–11, includes 'exceptionnelle'")
    indice = models.PositiveSmallIntegerField(help_text="Échelon's salary-calc representation")
    mutuelle = models.CharField(max_length=50, choices=MUTUELLE)
    position = models.CharField(max_length=25, choices=POSITIONS, default="en_activite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.civil_servant} — {self.grade} / Echelon {self.echelon} / Indice {self.indice}"


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


# those models to keep the category -> garde-> echelle -> echellon data :

class Categorie(models.Model):
    code = models.SlugField(max_length=100, unique=True)   # "technicien", "administrateur"
    label = models.CharField(max_length=200, blank=True)     # optional display name

    def __str__(self):
        return self.code


class Grade(models.Model):
    categorie = models.ForeignKey(Categorie, related_name="grades", on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    label = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("categorie", "code")

    def __str__(self):
        return f"{self.categorie.code}/{self.code}"


class EchelonIndice(models.Model):
    grade = models.ForeignKey(Grade, related_name="echelons", on_delete=models.CASCADE)
    echelon = models.PositiveSmallIntegerField()
    indice = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("grade", "echelon")
        ordering = ["grade", "echelon"]

    def __str__(self):
        return f"{self.grade} ech.{self.echelon} = {self.indice}"