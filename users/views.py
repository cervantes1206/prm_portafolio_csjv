from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def redirect_after_login(request):
    user = request.user

    if user.role == "student":
        return redirect("student_dashboard")

    if user.role == "admin":
        return redirect("/admin/")

    return redirect("student_dashboard")