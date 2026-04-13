from django.contrib import admin
from .models import Student, Strength, Talent, Interest


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "documento",
        "nombre_completo",
        "correo_institucional",
        "user",
        "grado",
        "grupo",
        "sede",
        "estado",
    )
    search_fields = (
        "documento",
        "nombre_completo",
        "correo_institucional",
        "codigo_estudiante",
    )
    list_filter = ("grado", "grupo", "sede", "school_level", "estado")


@admin.register(Strength)
class StrengthAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "student",
        "nivel_desarrollo",
        "visible_dashboard",
        "created_at",
    )
    search_fields = (
        "titulo",
        "descripcion",
        "student__nombre_completo",
        "student__documento",
    )
    list_filter = ("nivel_desarrollo", "visible_dashboard", "student__grado", "student__grupo")


@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "student",
        "nivel_desarrollo",
        "visible_dashboard",
        "created_at",
    )
    search_fields = (
        "titulo",
        "descripcion",
        "student__nombre_completo",
        "student__documento",
    )
    list_filter = ("nivel_desarrollo", "visible_dashboard", "student__grado", "student__grupo")


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "student",
        "nivel_interes",
        "visible_dashboard",
        "created_at",
    )
    search_fields = (
        "titulo",
        "descripcion",
        "student__nombre_completo",
        "student__documento",
    )
    list_filter = ("nivel_interes", "visible_dashboard", "student__grado", "student__grupo")