from django.conf import settings
from django.db import models


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
    nivel_desarrollo = models.PositiveSmallIntegerField(choices=DEVELOPMENT_LEVEL_CHOICES, default=3)
    visible_dashboard = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "strengths"
        verbose_name = "fortaleza"
        verbose_name_plural = "fortalezas"
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
    nivel_desarrollo = models.PositiveSmallIntegerField(choices=DEVELOPMENT_LEVEL_CHOICES, default=3)
    visible_dashboard = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "talents"
        verbose_name = "talento"
        verbose_name_plural = "talentos"
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
    nivel_interes = models.PositiveSmallIntegerField(choices=DEVELOPMENT_LEVEL_CHOICES, default=3)
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