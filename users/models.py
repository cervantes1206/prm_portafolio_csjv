from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("leader", "Líder"),
        ("teacher", "Docente"),
        ("student", "Estudiante"),
    ]

    SCHOOL_LEVEL_CHOICES = [
        ("preschool", "Preschool"),
        ("elementary", "Elementary"),
        ("middle", "Middle"),
        ("upper", "Upper"),
        ("high", "High"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    school_level = models.CharField(
        max_length=20,
        choices=SCHOOL_LEVEL_CHOICES,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["email"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email