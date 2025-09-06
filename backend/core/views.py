# backend/core/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse

# main page
def home(request):
    # matches: backend/core/templates/core/home.html
    return render(request, "core/home.html")


# for student section
def student_search(request):
    return render(request, "core/student/search.html")

# for employer section
def employer_positions(request):
    return render(request, "core/employer/positions.html")

# for faculty section
def faculty_dashboard(request):
    return render(request, "core/faculty/dashboard.html")

# (optional) fake login/logout for later
def login_view(request):
    return HttpResponse("Login placeholder")
def logout_view(request):
    return redirect("home")
