from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StrengthForm, StudentPhotoForm, TalentForm, InterestForm
from .models import Student, Strength, Talent, Interest


@login_required
def strength_list(request):
    student = get_object_or_404(Student, user=request.user)
    strengths = student.strengths.all().order_by("-nivel_desarrollo", "titulo")
    return render(request, "students/strength_list.html", {"student": student, "strengths": strengths})


@login_required
def strength_create(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = StrengthForm(request.POST)
        if form.is_valid():
            strength = form.save(commit=False)
            strength.student = student
            strength.save()
            return redirect("strength_list")
    else:
        form = StrengthForm()
    return render(request, "students/strength_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": False,
    })


@login_required
def strength_update(request, pk):
    student = get_object_or_404(Student, user=request.user)
    strength = get_object_or_404(Strength, pk=pk, student=student)
    if request.method == "POST":
        form = StrengthForm(request.POST, instance=strength)
        if form.is_valid():
            form.save()
            return redirect("strength_list")
    else:
        form = StrengthForm(instance=strength)
    return render(request, "students/strength_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": True,
    })


@login_required
def strength_delete(request, pk):
    student = get_object_or_404(Student, user=request.user)
    strength = get_object_or_404(Strength, pk=pk, student=student)
    if request.method == "POST":
        strength.delete()
    return redirect("strength_list")


@login_required
def talent_list(request):
    student = get_object_or_404(Student, user=request.user)
    talents = student.talents.all().order_by("-nivel_desarrollo", "titulo")
    return render(request, "students/talent_list.html", {"student": student, "talents": talents})


@login_required
def talent_create(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = TalentForm(request.POST)
        if form.is_valid():
            talent = form.save(commit=False)
            talent.student = student
            talent.save()
            return redirect("talent_list")
    else:
        form = TalentForm()
    return render(request, "students/talent_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": False,
    })


@login_required
def talent_update(request, pk):
    student = get_object_or_404(Student, user=request.user)
    talent = get_object_or_404(Talent, pk=pk, student=student)
    if request.method == "POST":
        form = TalentForm(request.POST, instance=talent)
        if form.is_valid():
            form.save()
            return redirect("talent_list")
    else:
        form = TalentForm(instance=talent)
    return render(request, "students/talent_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": True,
    })


@login_required
def talent_delete(request, pk):
    student = get_object_or_404(Student, user=request.user)
    talent = get_object_or_404(Talent, pk=pk, student=student)
    if request.method == "POST":
        talent.delete()
    return redirect("talent_list")


@login_required
def interest_list(request):
    student = get_object_or_404(Student, user=request.user)
    interests = student.interests.all().order_by("-nivel_interes", "titulo")
    return render(request, "students/interest_list.html", {"student": student, "interests": interests})


@login_required
def interest_create(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.student = student
            interest.save()
            return redirect("interest_list")
    else:
        form = InterestForm()
    return render(request, "students/interest_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": False,
    })


@login_required
def interest_update(request, pk):
    student = get_object_or_404(Student, user=request.user)
    interest = get_object_or_404(Interest, pk=pk, student=student)
    if request.method == "POST":
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect("interest_list")
    else:
        form = InterestForm(instance=interest)
    return render(request, "students/interest_form.html", {
        "student": student,
        "form": form,
        "modo_edicion": True,
    })


@login_required
def interest_delete(request, pk):
    student = get_object_or_404(Student, user=request.user)
    interest = get_object_or_404(Interest, pk=pk, student=student)
    if request.method == "POST":
        interest.delete()
    return redirect("interest_list")


@login_required
def student_photo_update(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = StudentPhotoForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = StudentPhotoForm(instance=student)
    return render(request, "students/photo_form.html", {"student": student, "form": form})