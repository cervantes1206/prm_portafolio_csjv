from django.conf import settings
from django.db import models


class Archetype(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "archetypes"
        verbose_name = "arquetipo"
        verbose_name_plural = "arquetipos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro"),
    ]

    STATUS_CHOICES = [
        ("Confirmado", "Confirmado"),
        ("Pendiente", "Pendiente"),
        ("Retirado", "Retirado"),
        ("Inactivo", "Inactivo"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="student_profile",
        blank=True,
        null=True,
    )

    documento = models.CharField(max_length=30, unique=True)
    tipo_documento = models.CharField(max_length=50)
    codigo_estudiante = models.CharField(max_length=30, unique=True)

    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    nombre_completo = models.CharField(max_length=255)

    foto = models.ImageField(upload_to="students/photos/", blank=True, null=True)
    foto_pos_x = models.PositiveSmallIntegerField(default=50)
    foto_pos_y = models.PositiveSmallIntegerField(default=50)

    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=20, choices=GENDER_CHOICES)

    grado = models.CharField(max_length=20)
    grupo = models.CharField(max_length=10)
    anio = models.PositiveIntegerField()
    sede = models.CharField(max_length=100)
    school_level = models.CharField(max_length=30)

    arquetipo = models.ForeignKey(
        Archetype,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    nombre_padre = models.CharField(max_length=255, blank=True, null=True)
    telefono_padre = models.CharField(max_length=30, blank=True, null=True)
    nombre_madre = models.CharField(max_length=255, blank=True, null=True)
    telefono_madre = models.CharField(max_length=30, blank=True, null=True)

    correo_institucional = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    eps = models.CharField(max_length=100, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Confirmado")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students"
        verbose_name = "estudiante"
        verbose_name_plural = "estudiantes"
        ordering = ["grado", "grupo", "apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombre_completo} - {self.grado}{self.grupo}"


class Strength(models.Model):
    DEVELOPMENT_LEVEL_CHOICES = [
        (1, "Inicial"),
        (2, "Básico"),
        (3, "Intermedio"),
        (4, "Alto"),
        (5, "Sobresaliente"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="strengths",
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    nivel_desarrollo = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default=3
    )
    visible_dashboard = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "strengths"
        verbose_name = "habilidad socioemocional"
        verbose_name_plural = "habilidades socioemocionales"
        ordering = ["-nivel_desarrollo", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.student.nombre_completo}"

    def save(self, *args, **kwargs):
        if self.titulo:
            self.titulo = self.titulo.upper().strip()
        super().save(*args, **kwargs)


class Talent(models.Model):
    DEVELOPMENT_LEVEL_CHOICES = [
        (1, "Inicial"),
        (2, "Básico"),
        (3, "Intermedio"),
        (4, "Alto"),
        (5, "Sobresaliente"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="talents",
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    nivel_desarrollo = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default=3
    )
    visible_dashboard = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "talents"
        verbose_name = "habilidad técnica"
        verbose_name_plural = "habilidades técnicas"
        ordering = ["-nivel_desarrollo", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.student.nombre_completo}"

    def save(self, *args, **kwargs):
        if self.titulo:
            self.titulo = self.titulo.upper().strip()
        super().save(*args, **kwargs)


class Interest(models.Model):
    DEVELOPMENT_LEVEL_CHOICES = [
        (1, "Muy bajo"),
        (2, "Bajo"),
        (3, "Medio"),
        (4, "Alto"),
        (5, "Muy alto"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="interests",
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    nivel_interes = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default=3
    )
    visible_dashboard = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "interests"
        verbose_name = "interés"
        verbose_name_plural = "intereses"
        ordering = ["-nivel_interes", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.student.nombre_completo}"

    def save(self, *args, **kwargs):
        if self.titulo:
            self.titulo = self.titulo.upper().strip()
        super().save(*args, **kwargs)


class SocioEmotionalSkill(models.Model):
    DEVELOPMENT_LEVEL_CHOICES = [
        (1, "Inicial"),
        (2, "Básico"),
        (3, "Intermedio"),
        (4, "Alto"),
        (5, "Sobresaliente"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="socio_emotional_skills",
    )
    arquetipo = models.ForeignKey(
        Archetype,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="socio_emotional_skills",
    )
    titulo = models.CharField(max_length=150)
    idg_dimension = models.CharField(max_length=80, blank=True, null=True)
    nivel_desarrollo = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default=3
    )
    mentor_nivel = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    visible_dashboard = models.BooleanField(default=True)
    comentario_estudiante = models.TextField(blank=True, null=True)
    comentario_mentor = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_socio_emotional_skills",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "socio_emotional_skills"
        verbose_name = "habilidad socioemocional nueva"
        verbose_name_plural = "habilidades socioemocionales nuevas"
        ordering = ["-nivel_desarrollo", "titulo"]
        unique_together = ("student", "titulo")

    def __str__(self):
        return f"{self.titulo} - {self.student.nombre_completo}"

    def save(self, *args, **kwargs):
        if self.titulo:
            self.titulo = self.titulo.strip()
        super().save(*args, **kwargs)


class TechnicalSkill(models.Model):
    DEVELOPMENT_LEVEL_CHOICES = [
        (1, "Inicial"),
        (2, "Básico"),
        (3, "Intermedio"),
        (4, "Alto"),
        (5, "Sobresaliente"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="technical_skills",
    )
    arquetipo = models.ForeignKey(
        Archetype,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="technical_skills",
    )
    titulo = models.CharField(max_length=150)
    school_year = models.PositiveIntegerField(default=2026)
    nivel_desarrollo = models.PositiveSmallIntegerField(
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default=1
    )
    progreso_porcentaje = models.PositiveSmallIntegerField(default=0)
    visible_dashboard = models.BooleanField(default=True)
    ruta_aprendizaje = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "technical_skills"
        verbose_name = "habilidad técnica nueva"
        verbose_name_plural = "habilidades técnicas nuevas"
        ordering = ["-nivel_desarrollo", "titulo"]
        unique_together = ("student", "titulo", "school_year")

    def __str__(self):
        return f"{self.titulo} - {self.student.nombre_completo} ({self.school_year})"

    def save(self, *args, **kwargs):
        if self.titulo:
            self.titulo = self.titulo.strip()
        super().save(*args, **kwargs)