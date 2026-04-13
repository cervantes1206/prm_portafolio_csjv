from django.db import models

# Create your models here.

from students.models import Student


class Strength(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='strengths')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    nivel_desarrollo = models.PositiveIntegerField(default=1)
    visible_dashboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-nivel_desarrollo', '-created_at']

    def __str__(self):
        return f"{self.student.nombre_completo} - {self.nombre}"

    @property
    def porcentaje(self):
        return round((self.nivel_desarrollo / 5) * 100, 2)


class Talent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='talents')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    anio_inicio = models.PositiveIntegerField(blank=True, null=True)
    area = models.CharField(max_length=120)
    logros_relacionados = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='talents/', blank=True, null=True)
    visible_dashboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.nombre_completo} - {self.nombre}"


class Interest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='interests')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='interests/', blank=True, null=True)
    visible_dashboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.nombre_completo} - {self.nombre}"


class Value(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='values')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    visible_dashboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.nombre_completo} - {self.nombre}"