from django.urls import path
from . import views

urlpatterns = [

    # home
    path("", views.home, name="home"),

    # Students
    path("students/login", views.students_login, name="students_login"),
    path("students/register", views.students_register, name="students_register"),

    # Faculty
    path("faculty/login", views.faculty_login, name="faculty_login"),
    path("faculty/register", views.faculty_register, name="faculty_register"),

    # Employers
    path("employers/login", views.employer_login, name="employer_login"),
    path("employers/register", views.employer_register, name="employer_register"),


    # portals
    path("students/", views.student_portal, name="student_portal"),
    path("employers/", views.employer_portal, name="employer_portal"),
    path("faculty/", views.faculty_portal, name="faculty_portal"),

    # employers
    path("employers/list/", views.employer_list, name="employer_list"),
    path("employers/<int:pk>/", views.employer_detail, name="employer_detail"),
    path("employers/<int:pk>/edit/", views.employer_edit, name="employer_edit"),

   
    # positions
    path("positions/create/", views.position_create, name="position_create"),
    path("positions/<int:pk>/", views.position_detail, name="position_detail"),
    path("positions/<int:pk>/edit/", views.position_edit, name="position_edit"),
    path("positions/<int:pk>/status/<str:new_status>/", views.position_change_status, name="position_change_status"),

    # hiring flow
    path("positions/<int:pk>/mark-pending/", views.position_mark_pending, name="position_mark_pending"),
]
