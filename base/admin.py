from django.contrib import admin
from .models import Doctor, Appointment, Patient
from .models import Profile
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Profile)
admin.site.register(Permission)
