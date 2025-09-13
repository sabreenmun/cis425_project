# backend/core/views.py
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EmployerForm, PositionForm, MarkPendingForm, EmployerRegisterForm
from .models import Employer, Position, Application, Student, Coop

# home page
def home(request):
    return render(request, "core/home.html")

# portals
def student_portal(request):
    return render(request, "core/students/portal.html")
def employer_portal(request):
    return render(request, "core/employers/portal.html")
def faculty_portal(request):
    return render(request, "core/faculty/portal.html")

def students_login(request):
    return render(request, "core/students/login.html")
def students_register(request):
    return render(request, "core/students/register.html")
# Faculty views
def faculty_login(request):
    return render(request, "core/faculty/login.html")

def faculty_register(request):
    return render(request, "core/faculty/register.html")

def employer_login(request):
    return render(request, "core/employers/login.html")

def employer_register(request):
    return render(request, "core/employers/register.html", {"form": form})

def employer_list(request):
    employers = Employer.objects.all().order_by("name")
    return render(request, "core/employers/list.html", {"employers": employers})

def employer_register(request):
    if request.method == "POST":
        form = EmployerRegisterForm(request.POST)
        if form.is_valid():
            # Create and save the employer
            Employer.objects.create(
                name=form.cleaned_data["company_name"],
                contact_name=form.cleaned_data["contact_name"],
                contact_email=form.cleaned_data["email"],
                contact_phone=form.cleaned_data["phone"],
                # Optionally hash the password
                password=make_password(form.cleaned_data["password"])
            )
            return redirect("employer_login")  # Redirect after successful registration
    else:
        form = EmployerRegisterForm()
    
    return render(request, "employers/register.html", {"form": form})

def employer_detail(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    positions = employer.positions.all().order_by("-created_at")
    return render(request, "core/employers/detail.html", {"employer": employer, "positions": positions})

def employer_edit(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    if request.method == "POST":
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, "Employer updated.")
            return redirect("employer_detail", pk=employer.pk)
    else:
        form = EmployerForm(instance=employer)
    return render(request, "core/employers/form.html", {"form": form, "title": f"Edit {employer.name}"})

# position functionality
def position_create(request):
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            pos = form.save()
            messages.success(request, "Position created.")
            return redirect("position_detail", pk=pos.pk)
    else:
        form = PositionForm()
    return render(request, "core/positions/form.html", {"form": form, "title": "Create Position"})

def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, "Position updated.")
            return redirect("position_detail", pk=position.pk)
    else:
        form = PositionForm(instance=position)
    return render(request, "core/positions/form.html", {"form": form, "title": f"Edit {position.title}"})

def position_detail(request, pk):
    position = get_object_or_404(Position, pk=pk)
    apps = position.applications.select_related("student").order_by("-applied_at")
    return render(request, "core/positions/detail.html", {
        "position": position,
        "applications": apps,
        "pending_allowed": position.status in ("open", "pending"),
    })

def position_change_status(request, pk, new_status):
    position = get_object_or_404(Position, pk=pk)
    if new_status not in dict(Position.STATUS):
        messages.error(request, "Invalid status.")
        return redirect("position_detail", pk=position.pk)
    position.status = new_status
    position.save(update_fields=["status"])
    messages.success(request, f"Position marked as {new_status}.")
    return redirect("position_detail", pk=position.pk)

# hiring functionality

def _is_eligible_for_coop(student: Student, position: Position) -> bool:
    if float(student.gpa) < 2.0:
        return False
    if position.weeks < 7:
        return False
    if (position.weeks * position.hours_per_week) < 140:
        return False
    if student.is_transfer:
        return student.semesters_completed >= 1
    return student.semesters_completed >= 2

@transaction.atomic
def position_mark_pending(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == "POST":
        form = MarkPendingForm(request.POST, request.FILES)
        if form.is_valid():
            sel_student = form.cleaned_data["selected_student"]
            offer = form.cleaned_data["offer_letter"]

            position.selected_student = sel_student
            position.offer_letter = offer
            position.status = "pending"
            position.save()

            coop, _ = Coop.objects.get_or_create(student=sel_student, position=position)
            coop.eligible = _is_eligible_for_coop(sel_student, position)
            coop.indicated_interest = False
            coop.save()

            try:
                if coop.eligible and sel_student.email:
                    send_mail(
                        subject="Co-op Eligibility Notice",
                        message=(
                            f"Hi {sel_student.name},\n\n"
                            f"You've been selected for the position '{position.title}' at {position.employer.name}.\n"
                            "You are ELIGIBLE for co-op credit. Please log in to the portal and indicate your interest."
                        ),
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                        recipient_list=[sel_student.email],
                        fail_silently=True,
                    )
            except Exception:
                pass

            messages.success(request, "Position marked as pending and eligibility processed.")
            return redirect("position_detail", pk=position.pk)
    else:
        form = MarkPendingForm()

    applied_student_ids = position.applications.values_list("student_id", flat=True)
    form.fields["selected_student"].queryset = Student.objects.filter(id__in=applied_student_ids)

    return render(request, "core/positions/mark_pending.html", {
        "position": position,
        "form": form
    })