import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from sdau.models import Secteur, ZoneSdau, SecteurZone


class Command(BaseCommand):
    help = "Importer Secteur, ZoneSdau et SecteurZone depuis CSV"

    def lire_csv(self, chemin, delimiter=','):
        """
        Essaie plusieurs encodages pour lire un CSV.
        Retourne la liste des lignes.
        """
        encodings = ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1']
        last_error = None

        for enc in encodings:
            try:
                with open(chemin, newline='', encoding=enc) as file:
                    reader = list(csv.DictReader(file, delimiter=delimiter))
                    return reader, enc
            except Exception as e:
                last_error = e

        raise last_error

    def handle(self, *args, **kwargs):
        base_path = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\data"
        fichiers = {
            "secteur": os.path.join(base_path, "secteur.csv"),
            "zone": os.path.join(base_path, "zone_sdau.csv"),
            "secteur_zone": os.path.join(base_path, "secteur_zone.csv")
        }

        # -----------------------------
        # Import Secteurs
        # -----------------------------
        if not os.path.exists(fichiers["secteur"]):
            self.stdout.write(self.style.ERROR("❌ Fichier secteur.csv introuvable"))
        else:
            try:
                reader, enc = self.lire_csv(fichiers["secteur"], delimiter=',')
                self.stdout.write(self.style.NOTICE(f"📄 Secteur : {len(reader)} lignes détectées (encodage: {enc})"))
                succes_count = 0

                for row in reader:
                    try:
                        geom_wkt = row.get('geom_wkt') or row.get('geom')
                        if not geom_wkt:
                            raise ValueError("Colonne geom_wkt/geom introuvable dans le CSV")

                        geom = GEOSGeometry(geom_wkt)
                        geom.srid = 4326

                        Secteur.objects.update_or_create(
                            id_secteur=int(row['id_secteur']),
                            defaults={
                                'nom_secteur': row['nom_secteur'].strip(),
                                'geom': geom
                            }
                        )
                        succes_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur Secteur: {row} -> {e}"))

                self.stdout.write(self.style.SUCCESS(f"✅ Secteur importé : {succes_count}/{len(reader)} lignes"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Impossible de lire secteur.csv : {e}"))

        # -----------------------------
        # Import Zones SDAU
        # -----------------------------
        if not os.path.exists(fichiers["zone"]):
            self.stdout.write(self.style.ERROR("❌ Fichier zone_sdau.csv introuvable"))
        else:
            try:
                reader, enc = self.lire_csv(fichiers["zone"], delimiter=',')
                self.stdout.write(self.style.NOTICE(f"📄 Zone SDAU : {len(reader)} lignes détectées (encodage: {enc})"))
                succes_count = 0

                for row in reader:
                    try:
                        geom_wkt = row.get('geom_wkt') or row.get('geom')
                        if not geom_wkt:
                            raise ValueError("Colonne geom_wkt/geom introuvable dans le CSV")

                        geom = GEOSGeometry(geom_wkt)
                        geom.srid = 4326

                        ZoneSdau.objects.update_or_create(
                            id_zone=int(row['id_zone']),
                            defaults={
                                'zone_sdau': row['zone_sdau'].strip(),
                                'aire_ha': float(row['aire_ha']),
                                'type_zone': row['type_zone'].strip(),
                                'statut_amenagement': row['statut_amenagement'].strip(),
                                'geom': geom
                            }
                        )
                        succes_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur Zone SDAU: {row} -> {e}"))

                self.stdout.write(self.style.SUCCESS(f"✅ Zone SDAU importé : {succes_count}/{len(reader)} lignes"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Impossible de lire zone_sdau.csv : {e}"))

        # -----------------------------
        # Import SecteurZone
        # -----------------------------
        if not os.path.exists(fichiers["secteur_zone"]):
            self.stdout.write(self.style.ERROR("❌ Fichier secteur_zone.csv introuvable"))
        else:
            try:
                reader, enc = self.lire_csv(fichiers["secteur_zone"], delimiter=';')
                self.stdout.write(self.style.NOTICE(f"📄 SecteurZone : {len(reader)} lignes détectées (encodage: {enc})"))
                succes_count = 0

                for row in reader:
                    try:
                        secteur = Secteur.objects.get(id_secteur=int(row['id_secteur']))
                        zone = ZoneSdau.objects.get(id_zone=int(row['id_zone']))

                        SecteurZone.objects.get_or_create(
                            id_secteur=secteur,
                            id_zone=zone
                        )
                        succes_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur SecteurZone: {row} -> {e}"))

                self.stdout.write(self.style.SUCCESS(f"✅ SecteurZone importé : {succes_count}/{len(reader)} lignes"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Impossible de lire secteur_zone.csv : {e}"))

        self.stdout.write(self.style.SUCCESS("🎉 Import complet terminé !"))
