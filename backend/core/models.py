from django.db import models

class Employer(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    contact_name = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    def __str__(self): return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=120, blank=True)
    major = models.CharField(max_length=120, blank=True)
    credits_in_major = models.IntegerField(default=0)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    start_term = models.CharField(max_length=40, blank=True)
    is_transfer = models.BooleanField(default=False)
    semesters_completed = models.IntegerField(default=0)
    def __str__(self): return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    department = models.CharField(max_length=120)
    def __str__(self): return f"{self.name} ({self.department})"

class Position(models.Model):
    STATUS = (("open","open"),("pending","pending"),("closed","closed"))
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    weeks = models.IntegerField(default=0)
    hours_per_week = models.IntegerField(default=0)
    location = models.CharField(max_length=200, blank=True)
    majors_of_interest = models.CharField(max_length=200, blank=True)
    required_skills = models.CharField(max_length=300, blank=True)
    preferred_skills = models.CharField(max_length=300, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.title} @ {self.employer.name}"

class Application(models.Model):
    STATUS = (("submitted","submitted"),("reviewed","reviewed"),
              ("interviewing","interviewing"),("offered","offered"),("rejected","rejected"))
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default="submitted")
    applied_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("position","student")
    def __str__(self): return f"{self.student.name} -> {self.position.title}"

class Coop(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    eligible = models.BooleanField(default=False)
    indicated_interest = models.BooleanField(default=False)
    summary_text = models.TextField(blank=True)
    grade = models.CharField(max_length=5, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"Co-op: {self.student.name} / {self.position.title}"