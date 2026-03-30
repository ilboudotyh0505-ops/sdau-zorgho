import csv
import os

from django.core.management.base import BaseCommand

from sdau.models import Secteur, SecteurZone, ZoneSdau


class Command(BaseCommand):
    help = 'Importer secteur_zone depuis CSV'

    def handle(self, *args, **kwargs):
        fichier_csv = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\data\secteur_zone.csv"

        if not os.path.exists(fichier_csv):
            self.stdout.write(self.style.ERROR("❌ Fichier CSV introuvable"))
            return

        with open(fichier_csv, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')  # Assure-toi que le CSV utilise ';'

            for row in reader:
                try:
                    # Récupération des instances avec les bons champs
                    secteur = Secteur.objects.get(id_secteur=row['id_secteur'])
                    zone = ZoneSdau.objects.get(id_zone=row['id_zone'])

                    # Création ou récupération de l'objet SecteurZone
                    SecteurZone.objects.get_or_create(
                        id_secteur=secteur,
                        id_zone=zone
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur: {row} -> {e}"))

        self.stdout.write(self.style.SUCCESS('✅ Import réussi'))