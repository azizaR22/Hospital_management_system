from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default="default.jpg", upload_to="profile_images")
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(null=False)
    special = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-updated"]

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    patient_type = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-updated"]

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-updated"]

    def __str__(self):
        return str(self.id)
