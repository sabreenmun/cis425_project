from django import forms
from .models import Employer, Position, Student



#Employee Forms!
class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ["name", "location", "website", "contact_name", "contact_email", "contact_phone"]

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = [
            "employer", "title", "description", "weeks", "hours_per_week", "location",
            "majors_of_interest", "required_skills", "preferred_skills", "salary", "status"
        ]

class MarkPendingForm(forms.Form):
    selected_student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=True,
        label="Selected Student"
    )
    offer_letter = forms.FileField(required=True, label="Offer Letter (PDF or image)")