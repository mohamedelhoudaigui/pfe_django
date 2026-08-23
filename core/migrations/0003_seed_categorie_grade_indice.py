from django.db import migrations


def seed_categorie_grade_indice(apps, schema_editor):
    Categorie = apps.get_model("core", "Categorie")
    Grade = apps.get_model("core", "Grade")
    EchelonIndice = apps.get_model("core", "EchelonIndice")

    # paste your full ECHELON_INDICE_TABLEAU dict here, unchanged
    
    for categorie_code, grades in TABLE.items():
        categorie, _ = Categorie.objects.get_or_create(
            code=categorie_code,
            defaults={"label": categorie_code.replace("_", " ").title()},
        )
        for grade_code, echelons in grades.items():
            grade, _ = Grade.objects.get_or_create(
                categorie=categorie,
                code=grade_code,
                defaults={"label": grade_code},
            )
            for echelon, indice in echelons.items():
                EchelonIndice.objects.get_or_create(
                    grade=grade,
                    echelon=echelon,
                    defaults={"indice": indice},
                )


def unseed_categorie_grade_indice(apps, schema_editor):
    Categorie = apps.get_model("core", "Categorie")
    Categorie.objects.all().delete()  # cascades to Grade -> EchelonIndice


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_categorie_alter_jobdetail_categorie_and_more"),  # match your actual filename
    ]

    operations = [
        migrations.RunPython(seed_categorie_grade_indice, unseed_categorie_grade_indice),
    ]