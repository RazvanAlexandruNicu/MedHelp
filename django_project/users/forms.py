from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from users.models import extendedUser, Appointment, Prescription

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'

class requestAppointmentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(widget = DateInput)
    time = forms.CharField(widget = TimeInput)
    class Meta:
            model=Appointment #or whatever object
            fields = ['description', 'date', 'time']
            widgets = { 'date' : DateInput(), 'time' : TimeInput()}

class PrescriptionForm(forms.ModelForm):
    patient = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
            model = Prescription #or whatever object
            fields = ['patient', 'description']

class DecideRequests(forms.Form):
    info = forms.CharField()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = extendedUser
        fields = ['username', 'firstname', 'lastname', 'email', 'medic_code', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        entry = cleaned_data.get('medic_code')
        qs = extendedUser.objects.filter(groups__name__in=['Medic'])
        found = 0
        for medic in qs:
            if medic.medic_code == entry:
                found = 1
                break
        if found == 0:
            raise ValidationError("No Medic with such code!")

class UserRegisterFormByAdmin(UserCreationForm):
    class Meta:
        model = extendedUser
        fields = ['username', 'firstname', 'lastname', 'email', 'medic_code', 'password1', 'password2', 'type']

    def clean(self):
        cleaned_data = super(UserRegisterFormByAdmin, self).clean()
        entry = cleaned_data.get('medic_code')
        qs = extendedUser.objects.filter(groups__name__in=['Medic'])
        found = 0
        for medic in qs:
            if medic.medic_code == entry:
                found = 1
                break
        if found == 1:
            raise ValidationError("There is already a medic with this code!")
