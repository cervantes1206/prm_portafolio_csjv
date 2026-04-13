import csv
import json
import unicodedata
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from students.models import Strength, Student, Talent


class Command(BaseCommand):
    help = (
        "Importa habilidades técnicas y socioemocionales desde CSV/XLSX con columnas: "
        "documento, correo_institucional, habilidades_tecnicas, habilidades_socioemocionales"
    )

    required_columns = [
        "documento",
        "correo_institucional",
        "habilidades_tecnicas",
        "habilidades_socioemocionales",
    ]

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Ruta del archivo CSV/XLSX")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Reemplaza las habilidades existentes del estudiante antes de cargar las nuevas.",
        )

    def handle(self, *args, **options):
        path = Path(options["file_path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        rows = self.load_rows(path)

        created_strengths = 0
        created_talents = 0
        not_found = 0

        for idx, row in enumerate(rows, start=2):
            documento = self.clean_value(row.get("documento"))
            correo = self.clean_value(row.get("correo_institucional"))

            if not documento and not correo:
                self.stdout.write(self.style.WARNING(f"Fila {idx}: sin documento/correo, omitida."))
                continue

            student = self.find_student(documento, correo)
            if not student:
                not_found += 1
                self.stdout.write(self.style.WARNING(f"Fila {idx}: sin estudiante asociado ({documento or correo})."))
                continue

            socioemocionales = self.parse_list(row.get("habilidades_socioemocionales"))
            tecnicas = self.parse_list(row.get("habilidades_tecnicas"))

            with transaction.atomic():
                if options["replace"]:
                    student.strengths.all().delete()
                    student.talents.all().delete()

                for item in socioemocionales:
                    _, created = Strength.objects.get_or_create(
                        student=student,
                        titulo=item,
                        defaults={
                            "descripcion": "Cargada desde archivo de administración.",
                            "nivel_desarrollo": 3,
                            "visible_dashboard": True,
                        },
                    )
                    if created:
                        created_strengths += 1

                for item in tecnicas:
                    _, created = Talent.objects.get_or_create(
                        student=student,
                        titulo=item,
                        defaults={
                            "descripcion": "Cargada desde archivo de administración.",
                            "nivel_desarrollo": 3,
                            "visible_dashboard": True,
                        },
                    )
                    if created:
                        created_talents += 1

        self.stdout.write(self.style.SUCCESS("Importación de habilidades finalizada."))
        self.stdout.write(f"Habilidades socioemocionales procesadas: {created_strengths}")
        self.stdout.write(f"Habilidades técnicas procesadas: {created_talents}")
        self.stdout.write(f"Estudiantes no encontrados: {not_found}")

    def load_rows(self, path):
        suffix = path.suffix.lower()
        if suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as file:
                sample = file.read(4096)
                file.seek(0)
                delimiter = self.detect_csv_delimiter(sample)
                reader = csv.DictReader(file, delimiter=delimiter)
                return self.normalize_rows(reader)

        if suffix == ".xlsx":
            try:
                import openpyxl
            except ImportError as exc:
                raise CommandError(
                    "Para leer archivos XLSX debes instalar openpyxl (pip install openpyxl)."
                ) from exc

            workbook = openpyxl.load_workbook(path, data_only=True)
            sheet = workbook.active
            headers = [self.clean_header(cell.value) for cell in sheet[1]]
            data = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                data.append({headers[i]: row[i] for i in range(len(headers))})
            return self.normalize_rows(data)

        raise CommandError("Formato no soportado. Usa CSV o XLSX.")

    def normalize_rows(self, rows):
        normalized = []
        for row in rows:
            normalized_row = {self.clean_header(k): v for k, v in row.items()}
            normalized.append(normalized_row)

        if not normalized:
            raise CommandError("El archivo no contiene registros.")

        missing = [c for c in self.required_columns if c not in normalized[0].keys()]
        if missing:
            raise CommandError(f"Faltan columnas requeridas: {', '.join(missing)}")

        return normalized

    def parse_list(self, raw_value):
        raw_value = self.clean_value(raw_value)
        if not raw_value:
            return []

        if isinstance(raw_value, list):
            return [str(item).strip() for item in raw_value if str(item).strip()]

        text = str(raw_value).strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                pass
        elif text.startswith("{"):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    extracted = parsed.get("items") or parsed.get("skills") or parsed.get("habilidades")
                    if isinstance(extracted, list):
                        return [str(item).strip() for item in extracted if str(item).strip()]
            except json.JSONDecodeError:
                pass

        separators = ["|", ";", ","]
        for sep in separators:
            if sep in text:
                return [item.strip() for item in text.split(sep) if item.strip()]

        return [text]

    def find_student(self, documento, correo):
        if documento:
            student = Student.objects.filter(documento=documento).first()
            if student:
                return student

        if correo:
            student = Student.objects.filter(correo_institucional=correo).first()
            if student:
                return student

        return None

    def clean_header(self, value):
        if value is None:
            return ""

        text = str(value).strip().lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        return text.replace(" ", "_")

    def clean_value(self, value):
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def detect_csv_delimiter(self, sample):
        try:
            return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
        except csv.Error:
            return ","
