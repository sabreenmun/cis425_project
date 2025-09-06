from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # student
    path("student/search/", views.student_search, name="student_search"),

    # employer
    path("employer/positions/", views.employer_positions, name="employer_positions"),

    # faculty
    path("faculty/dashboard/", views.faculty_dashboard, name="faculty_dashboard"),
]
