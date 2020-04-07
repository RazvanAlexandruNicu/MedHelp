from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import extendedUser


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField()
    class Meta:
        model = extendedUser
        fields = ['username', 'email', 'medic_code', 'password1', 'password2']

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
        fields = ['username', 'email', 'medic_code', 'password1', 'password2', 'type']

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
