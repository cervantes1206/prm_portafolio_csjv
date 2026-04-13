import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from students.models import Student


@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    strengths_queryset = (
        student.strengths
        .filter(visible_dashboard=True)
        .order_by("-nivel_desarrollo", "titulo")[:5]
    )

    talents_queryset = (
        student.talents
        .filter(visible_dashboard=True)
        .order_by("-nivel_desarrollo", "titulo")[:5]
    )

    interests_queryset = (
        student.interests
        .filter(visible_dashboard=True)
        .order_by("-nivel_interes", "titulo")[:5]
    )

    strengths = []
    radar_labels = []
    radar_values = []

    for strength in strengths_queryset:
        percentage = int((strength.nivel_desarrollo / 5) * 100)
        strengths.append(
            {
                "titulo": strength.titulo.upper(),
                "porcentaje": percentage,
            }
        )
        radar_labels.append(strength.titulo.upper())
        radar_values.append(strength.nivel_desarrollo)

    talents = []
    talent_labels = []
    talent_values = []

    for talent in talents_queryset:
        percentage = int((talent.nivel_desarrollo / 5) * 100)
        talents.append(
            {
                "titulo": talent.titulo.upper(),
                "porcentaje": percentage,
            }
        )
        talent_labels.append(talent.titulo.upper())
        talent_values.append(percentage)

    interests = []
    interest_labels = []
    interest_values = []

    for interest in interests_queryset:
        percentage = int((interest.nivel_interes / 5) * 100)
        interests.append(
            {
                "titulo": interest.titulo.upper(),
                "porcentaje": percentage,
            }
        )
        interest_labels.append(interest.titulo.upper())
        interest_values.append(percentage)

    context = {
        "student": student,
        "strengths": strengths,
        "talents": talents,
        "interests": interests,
        "radar_labels_json": json.dumps(radar_labels),
        "radar_values_json": json.dumps(radar_values),
        "talent_labels_json": json.dumps(talent_labels),
        "talent_values_json": json.dumps(talent_values),
        "interest_labels_json": json.dumps(interest_labels),
        "interest_values_json": json.dumps(interest_values),
    }
    return render(request, "dashboard/student_dashboard.html", context)
