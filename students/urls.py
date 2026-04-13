from django.urls import path
from .views import (
    strength_list, strength_create, strength_update, strength_delete,
    talent_list, talent_create, talent_update, talent_delete,
    interest_list, interest_create, interest_update, interest_delete,
    student_photo_update,
)

urlpatterns = [
    path("habilidades-socioemocionales/", strength_list, name="strength_list"),
    path("fortalezas/", strength_list),
    path("habilidades-socioemocionales/nueva/", strength_create, name="strength_create"),
    path("fortalezas/nueva/", strength_create),
    path("habilidades-socioemocionales/<int:pk>/editar/", strength_update, name="strength_update"),
    path("fortalezas/<int:pk>/editar/", strength_update),
    path("habilidades-socioemocionales/<int:pk>/eliminar/", strength_delete, name="strength_delete"),
    path("fortalezas/<int:pk>/eliminar/", strength_delete),

    path("inmersiones/", talent_list, name="talent_list"),
    path("talentos/", talent_list),
    path("inmersiones/nueva/", talent_create, name="talent_create"),
    path("talentos/nuevo/", talent_create),
    path("inmersiones/<int:pk>/editar/", talent_update, name="talent_update"),
    path("talentos/<int:pk>/editar/", talent_update),
    path("inmersiones/<int:pk>/eliminar/", talent_delete, name="talent_delete"),
    path("talentos/<int:pk>/eliminar/", talent_delete),

    path("intereses/", interest_list, name="interest_list"),
    path("intereses/nuevo/", interest_create, name="interest_create"),
    path("intereses/<int:pk>/editar/", interest_update, name="interest_update"),
    path("intereses/<int:pk>/eliminar/", interest_delete, name="interest_delete"),

    path("perfil/foto/", student_photo_update, name="student_photo_update"),
]