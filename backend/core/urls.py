from django.urls import path
from . import views

urlpatterns = [

    # home
    path("", views.home, name="home"),

    # portals
    path("student/", views.student_portal, name="student_portal"),
    path("employers/", views.employer_portal, name="employer_portal"),
    path("faculty/", views.faculty_portal, name="faculty_portal"),

     # employers
    path("employers/list/", views.employer_list, name="employer_list"),
    path("employers/create/", views.employer_create, name="employer_create"),
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
