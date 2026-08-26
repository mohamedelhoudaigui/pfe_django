from django import forms
from core.models import CivilServant, JobDetail, Categorie
from django.contrib.auth.models import User


class CivilServantRegistrationForm(forms.Form):
    # --- CivilServant fields ---
    CIN = forms.CharField(max_length=20, label="CIN")
    PPR = forms.CharField(max_length=50, label="PPR")
    nom = forms.CharField(max_length=100, label="Nom")
    prenom = forms.CharField(max_length=100, label="Prénom")
    date_de_naissance = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Date de naissance"
    )
    lieu_de_naissance = forms.CharField(max_length=100, label="Lieu de naissance")
    genre = forms.ChoiceField(choices=CivilServant.GENRE_CHOICES, label="Genre")
    situation_familiale = forms.ChoiceField(
        choices=CivilServant.SITUATION_FAMILIALE_CHOICES, label="Situation familiale"
    )
    n_enfants = forms.IntegerField(min_value=0, initial=0, label="Nombre d'enfants")
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Adresse")

    # --- JobDetail fields ---
    zone = forms.ChoiceField(choices=JobDetail.ZONES, label="Zone")

    categorie = forms.ChoiceField(label="Catégorie")
    grade = forms.ChoiceField(label="Grade", choices=[("", "---------")])
    echelon = forms.ChoiceField(label="Échelon", choices=[("", "---------")])
    echelle = forms.CharField(max_length=10, label="Échelle", required=False)

    mutuelle = forms.ChoiceField(choices=JobDetail.MUTUELLE, label="Mutuelle")

    # --- Login fields ---
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # categorie choices always come straight from the DB
        self.fields["categorie"].choices = [("", "---------")] + [
            (c.code, c.label or c.code) for c in Categorie.objects.order_by("code")
        ]

        # if grade/echelon were posted (re-render after a validation error),
        # rebuild their choices from the DB too, so re-selecting the same value works
        data = self.data if self.is_bound else {}
        categorie_code = data.get("categorie")
        grade_code = data.get("grade")

        if categorie_code:
            from core.models import Grade
            self.fields["grade"].choices = [("", "---------")] + [
                (g.code, g.label or g.code)
                for g in Grade.objects.filter(categorie__code=categorie_code).order_by("code")
            ]

        if categorie_code and grade_code:
            from core.models import EchelonIndice
            self.fields["echelon"].choices = [("", "---------")] + [
                (e.echelon, f"Échelon {e.echelon} — indice {e.indice}")
                for e in EchelonIndice.objects.filter(
                    grade__categorie__code=categorie_code, grade__code=grade_code
                ).order_by("echelon")
            ]

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.Select,)):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

    def clean_CIN(self):
        cin = self.cleaned_data["CIN"]
        if CivilServant.objects.filter(CIN=cin).exists():
            raise forms.ValidationError("A civil servant with this CIN already exists.")
        return cin

    def clean_PPR(self):
        ppr = self.cleaned_data["PPR"]
        if CivilServant.objects.filter(PPR=ppr).exists():
            raise forms.ValidationError("A civil servant with this PPR already exists.")
        return ppr

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def get_service_dicts(self) -> dict:
        data = self.cleaned_data

        civil_servant_data = {
            "CIN": data["CIN"],
            "PPR": data["PPR"],
            "nom": data["nom"],
            "prenom": data["prenom"],
            "date_de_naissance": data["date_de_naissance"],
            "lieu_de_naissance": data["lieu_de_naissance"],
            "genre": data["genre"],
            "situation_familiale": data["situation_familiale"],
            "n_enfants": data["n_enfants"],
            "address": data["address"],
        }

        job_detail_data = {
            "zone": data["zone"],
            "categorie": data["categorie"],
            "grade": data["grade"],
            "echelle": data.get("echelle") or "",
            "echelon": data["echelon"],
            "mutuelle": data["mutuelle"],
        }

        login_data = {
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],
        }

        return {
            "civil_servant_data": civil_servant_data,
            "job_detail_data": job_detail_data,
            "login_data": login_data,
        }