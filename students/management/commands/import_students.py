import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from students.models import Student
from users.models import User


class Command(BaseCommand):
    help = "Importa estudiantes desde un archivo CSV y crea sus usuarios automáticamente."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Ruta del archivo CSV a importar",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        path = Path(file_path)

        if not path.exists():
            raise CommandError(f"El archivo no existe: {file_path}")

        if path.suffix.lower() != ".csv":
            raise CommandError("Por ahora este comando solo admite archivos CSV.")

        created_students = 0
        created_users = 0
        updated_students = 0
        skipped_rows = 0

        required_columns = [
            "documento",
            "tipo_documento",
            "codigo_estudiante",
            "nombres",
            "apellidos",
            "nombre_completo",
            "fecha_nacimiento",
            "edad",
            "genero",
            "grado",
            "grupo",
            "anio",
            "sede",
            "school_level",
            "nombre_padre",
            "telefono_padre",
            "nombre_madre",
            "telefono_madre",
            "correo_institucional",
            "direccion",
            "eps",
            "fecha_ingreso",
            "estado",
        ]

        file = None
        reader = None
        detected_encoding = None
        detected_delimiter = None
        last_error = None

        encodings = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
        delimiters = [",", ";", "\t"]

        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    file = path.open(mode="r", encoding=encoding, newline="")
                    reader = csv.DictReader(file, delimiter=delimiter)
                    fieldnames = reader.fieldnames

                    if fieldnames:
                        normalized = [self.clean_header(col) for col in fieldnames]
                        missing_columns = [
                            col for col in required_columns if col not in normalized
                        ]

                        if len(missing_columns) < len(required_columns):
                            detected_encoding = encoding
                            detected_delimiter = delimiter
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Archivo leído con encoding: {encoding} y delimitador: {repr(delimiter)}"
                                )
                            )
                            break

                    file.close()
                    file = None

                except UnicodeDecodeError as error:
                    last_error = error
                    if file and not file.closed:
                        file.close()
                    file = None

            if reader is not None and detected_encoding is not None:
                break

        if detected_encoding is None or detected_delimiter is None:
            raise CommandError(
                f"No se pudo leer correctamente el archivo. Último error: {last_error}"
            )

        if file and not file.closed:
            file.close()

        file = path.open(mode="r", encoding=detected_encoding, newline="")
        reader = csv.DictReader(file, delimiter=detected_delimiter)

        original_fieldnames = reader.fieldnames or []
        normalized_fieldnames = [self.clean_header(col) for col in original_fieldnames]

        missing_columns = [col for col in required_columns if col not in normalized_fieldnames]
        if missing_columns:
            file.close()
            raise CommandError(
                f"Faltan columnas obligatorias en el CSV: {', '.join(missing_columns)}"
            )

        header_map = {
            self.clean_header(original): original
            for original in original_fieldnames
        }

        try:
            for row_number, row in enumerate(reader, start=2):
                try:
                    with transaction.atomic():
                        documento = self.get_value(row, header_map, "documento")
                        correo = self.get_value(row, header_map, "correo_institucional")

                        if not documento or not correo:
                            skipped_rows += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Fila {row_number}: omitida por falta de documento o correo."
                                )
                            )
                            continue

                        nombres = self.get_value(row, header_map, "nombres") or ""
                        apellidos = self.get_value(row, header_map, "apellidos") or ""

                        user, user_created = User.objects.get_or_create(
                            email=correo,
                            defaults={
                                "first_name": nombres,
                                "last_name": apellidos,
                                "role": "student",
                                "school_level": self.map_school_level(
                                    self.get_value(row, header_map, "school_level")
                                ),
                                "is_active": True,
                            },
                        )

                        if user_created:
                            user.set_password(documento)
                            user.save()
                            created_users += 1

                        student_defaults = {
                            "user": user,
                            "tipo_documento": self.get_value(row, header_map, "tipo_documento"),
                            "codigo_estudiante": self.get_value(row, header_map, "codigo_estudiante"),
                            "nombres": nombres,
                            "apellidos": apellidos,
                            "nombre_completo": self.get_value(row, header_map, "nombre_completo"),
                            "fecha_nacimiento": self.parse_date(
                                self.get_value(row, header_map, "fecha_nacimiento")
                            ),
                            "edad": self.parse_int(self.get_value(row, header_map, "edad")),
                            "genero": self.get_value(row, header_map, "genero"),
                            "grado": self.get_value(row, header_map, "grado"),
                            "grupo": self.get_value(row, header_map, "grupo"),
                            "anio": self.parse_int(self.get_value(row, header_map, "anio")),
                            "sede": self.get_value(row, header_map, "sede"),
                            "school_level": self.get_value(row, header_map, "school_level"),
                            "nombre_padre": self.get_value(row, header_map, "nombre_padre"),
                            "telefono_padre": self.get_value(row, header_map, "telefono_padre"),
                            "nombre_madre": self.get_value(row, header_map, "nombre_madre"),
                            "telefono_madre": self.get_value(row, header_map, "telefono_madre"),
                            "correo_institucional": correo,
                            "direccion": self.get_value(row, header_map, "direccion"),
                            "eps": self.get_value(row, header_map, "eps"),
                            "fecha_ingreso": self.parse_date(
                                self.get_value(row, header_map, "fecha_ingreso")
                            ),
                            "estado": self.get_value(row, header_map, "estado") or "Confirmado",
                        }

                        _, student_created = Student.objects.update_or_create(
                            documento=documento,
                            defaults=student_defaults,
                        )

                        if student_created:
                            created_students += 1
                        else:
                            updated_students += 1

                except Exception as error:
                    skipped_rows += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Fila {row_number}: error al importar -> {error}"
                        )
                    )
        finally:
            if file and not file.closed:
                file.close()

        self.stdout.write(self.style.SUCCESS("Importación finalizada."))
        self.stdout.write(f"Usuarios creados: {created_users}")
        self.stdout.write(f"Estudiantes creados: {created_students}")
        self.stdout.write(f"Estudiantes actualizados: {updated_students}")
        self.stdout.write(f"Filas omitidas/con error: {skipped_rows}")

    def clean_header(self, value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def get_value(self, row, header_map, normalized_key):
        original_key = header_map.get(normalized_key)
        if not original_key:
            return None
        return self.clean_value(row.get(original_key))

    def clean_value(self, value):
        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        if value.lower() in ["no disponible", "null", "none", "nan"]:
            return None

        return value

    def parse_date(self, value):
        value = self.clean_value(value)
        if not value:
            return None

        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Fecha inválida: {value}")

    def parse_int(self, value):
        value = self.clean_value(value)
        if not value:
            return None
        return int(str(value).strip())

    def map_school_level(self, value):
        value = self.clean_value(value)
        if not value:
            return None

        mapping = {
            "PRESCHOOL": "preschool",
            "ELEMENTARY": "elementary",
            "ELEMENTARY SCHOOL": "elementary",
            "MIDDLE": "middle",
            "MIDDLE SCHOOL": "middle",
            "UPPER": "upper",
            "UPPER SCHOOL": "upper",
            "HIGH": "high",
            "HIGH SCHOOL": "high",
        }

        return mapping.get(value.upper(), None)