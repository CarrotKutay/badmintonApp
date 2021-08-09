from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Select
from django.forms.widgets import TextInput, Textarea, SelectDateWidget

from .models import Player, Club, Discipline, Sport
from .widgets import FengyuanChenDatePickerInput
from django.utils import timezone


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PlayerCreateForm(forms.ModelForm):
    club = forms.ModelChoiceField(queryset=Club.objects.all(), widget=Select(), empty_label='choose club...')

    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'dob': SelectDateWidget
        }


class DisciplineCreateForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(), strip=True)
    sport = forms.ModelChoiceField(queryset=Sport.objects.all(), widget=Select(), empty_label='choose sport...')
    description = forms.CharField(widget=Textarea(), strip=True, required=False)

    class Meta:
        model = Discipline
        fields = '__all__'