from django.core.management.base import BaseCommand
from core.services.SeedService import SeedService


class Command(BaseCommand):
    help = "Seed categorie/grade/indice reference data, optionally with fake civil servants."

    def add_arguments(self, parser):
        parser.add_argument("--fake", type=int, default=0, help="Number of fake civil servants to create.")
        parser.add_argument("--force", action="store_true", help="Reseed reference data even if already present.")

    def handle(self, *args, **options):
        counts = SeedService.seed_categorie_grade_indice(force=options["force"])
        if counts["skipped"]:
            self.stdout.write("Reference data already present — skipped (use --force to reseed).")
        else:
            self.stdout.write(self.style.SUCCESS(f"Reference data seeded: {counts}"))

        if options["fake"] > 0:
            created = SeedService.seed_fake_civil_servants(options["fake"])
            self.stdout.write(self.style.SUCCESS(f"Created {created} fake civil servants."))