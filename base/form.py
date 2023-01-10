from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Patient, Appointment
from django import forms


class Doctorform(ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"


class Patientform(ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class Appoinmentform(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"


class Createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserEdit(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
