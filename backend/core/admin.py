from django.contrib import admin
from .models import Employer, Student, Faculty, Position, Application, Coop

admin.site.register(Employer)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Position)
admin.site.register(Application)
admin.site.register(Coop)
