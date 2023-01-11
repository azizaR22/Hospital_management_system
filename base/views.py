import queue
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Doctor, Patient, Appointment
from .form import Doctorform, Patientform, Appoinmentform, Createuserform, UserEdit
from .decorators import unautherized_user, allowed_users


# Create your views here.
# for showing signup/login button for admin
@unautherized_user
def loginPage(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")
            return redirect("login")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Invalid username or password")

    context = {"page": page}
    return render(request, "base/loginregister.html", context)


# for showing user registration
@unautherized_user
def user_register(request):
    form = Createuserform()
    if request.method == "POST":
        form = Createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="patients")
            user.groups.add(group)

            messages.success(request, "account was successfully created" + username)
            return redirect("login")
    context = {"form": form}
    return render(request, "base/user_registration.html", context)


@login_required(login_url="login")
def logoutuser(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    return redirect("login")


# -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_doctor(user):
    return user.groups.filter(name="doctor").exists()


def is_patient(user):
    return user.groups.filter(name="patient").exists()


@login_required(login_url="login")
def indexPage(request):
    doctors = Doctor.objects.all().count()
    patients = Patient.objects.all().count()
    appointments = Appointment.objects.all().count()
    dash_doctors = Doctor.objects.all()[:4]
    dash_patients = Patient.objects.all()[:4]

    context = {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments,
        "dash_doctors": dash_doctors,
        "dash_patients": dash_patients,
    }

    return render(request, "base/index.html", context)


@login_required(login_url="login")
@allowed_users(["admin", "doctor"])
def view_doc(request):
    doctors = Doctor.objects.all()
    p = {"doctors": doctors}
    return render(request, "base/view_doctor.html", p)


# -----------------Doctor START--------------------------------------------------------------------
@login_required(login_url="login")
@allowed_users(["admin"])
def delete_doc(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.delete()
    return redirect("view-doctor")


@login_required(login_url="login")
@allowed_users(["admin"])
def add_doctor(request):
    form = Doctorform()
    if request.method == "POST":
        form = Doctorform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"doctor was added succesfully")
            return redirect("view-doctor")
        else:
            messages.error(request, "error occured")
    context = {"form": form}
    return render(request, "base/add_doctor.html", context)


@login_required(login_url="login")
@allowed_users(["admin", "doctor"])
def updatedoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    form = Doctorform(instance=doctor)
    context = {"form": form, "doctor": doctor}
    if request.method == "POST":
        form = Doctorform(request.POST, instance=doctor)
        if form.is_valid:
            form.save()
            messages.success(request, f"patient was added succesfully")
            return redirect("view-doctor")
        else:
            messages.error(request, "error occured")
    return render(request, "base/add_doctor.html", context)


# -----------------Patient START--------------------------------------------------------------------
@login_required(login_url="login")
@allowed_users(["admin", "doctor", "patient"])
def view_patient(request):
    patients = Patient.objects.all()
    context = {"patients": patients}
    return render(request, "base/view_patient.html", context)


@login_required(login_url="login")
@allowed_users(["admin", "patient"])
def delete_patient(request, pk):
    patients = Patient.objects.get(id=pk)
    patients.delete()
    return redirect("view-patient")


@allowed_users(["admin", "patient", "doctor"])
@login_required(login_url="login")
def addPatient(request):
    form = Patientform()
    if request.method == "POST":
        form = Patientform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "patient added succesfully")
            return redirect("view-patient")
        else:
            messages.error(request, "error accured")
    context = {"form": form}
    return render(request, "base/add_patient.html", context)


@login_required(login_url="login")
@allowed_users(["admin"])
def updatepatient(request, pk):
    patient = Patient.objects.get(id=pk)
    form = Doctorform(instance=patient)
    context = {"form": form, "patient": patient}
    if request.method == "POST":
        context = {"form": form, "patient": patient}
        form = Patientform(request.POST, instance=patient)
        if form.is_valid:
            form.save()
            messages.success(request, f"patient was updated succesfully")
            return redirect("view-patient")
        else:
            messages.error(request, "error occured")

    return render(request, "base/add_patient.html", context)


# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url="login")
@allowed_users(["admin", "doctor"])
def view_Appoin(request):
    appointments = Appointment.objects.all()
    context = {"appointments": appointments}
    return render(request, "base/view_appoinments.html", context)


@login_required(login_url="login")
@allowed_users(["admin"])
def delete_Appoinments(request, pk):
    appointments = Appointment.objects.get(id=pk)
    appointments.delete()
    return redirect("view-appoinments")


@login_required(login_url="login")
@allowed_users(["admin", "doctor", "patient"])
def add_appoinments(request):
    doctors = Doctor.objects.all()
    patient2 = Patient.objects.all()
    if request.method == "POST":
        n = request.POST["doctor"]
        new_patient = request.POST["patient"]
        new_date = request.POST["date"]
        new_time = request.POST["time"]
        doctor = Doctor.objects.filter(name=n).first()
        patient = Patient.objects.filter(name=new_patient).first()
        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date=new_date,
            time=new_time,
        )
        messages.success(request, "appointment was added succesfully")
        return redirect("view-appoinments")
    else:
        messages.error(request, "error occured")
    context = {"doctor": doctors, "patient": patient2}
    return render(request, "base/add_appoinments.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "doctor"])
def updateappointments(request, pk):
    appointment = Appointment.objects.get(id=pk)
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":
        form = Appoinmentform(request.POST, instance=appointment)
        if form.is_valid:
            form.save()
            messages.success(request, f"appointment was succesfully updated")
            return redirect("view-appoinments")

    form = Appoinmentform(instance=appointment)
    context = {
        "form": form,
        "appointment": appointment,
        "doctors": doctors,
        "patients": patients,
    }

    return render(request, "base/update_appoint.html", context)


# -----------------VIEW START--------------------------------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def view_users(request):
    form = UserCreationForm()
    users = User.objects.all()
    context = {"users": users, "form": form}
    return render(request, "base/view_users.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect("view-users")


@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    group.delete()
    return redirect("view-groups")


@allowed_users(["admin", "patient", "doctor"])
@login_required(login_url="login")
def adduser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"user added succesfully")
            return redirect("view-users")
        else:
            messages.error(request, "error accured")
    context = {"form": form}
    return redirect("view-users")


# -----------------GROUP START--------------------------------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def view_group(request):
    perm = 0
    for i in request.user.groups.all():
        if i.name == "admin":
            perm = 1

    if perm == 0:
        messages.error(request, "access denied")

    groups = Group.objects.all().exclude(name="admin")
    context = {"groups": groups, "perm": perm}
    return render(request, "base/view_group.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def add_group(request):
    if request.method == "POST":

        name = request.POST.get("name")
        if name != "":
            if len(Group.objects.filter(name=name)) == 0:
                group = Group(name=name)
                group.save()

    return redirect("view-groups")


def edituser(request, pk):
    user = User.objects.get(id=pk)
    form = UserEdit(instance=user)
    if request.method == "POST":
        form = UserEdit(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect("view-users")
    context = {"form": form, "user": user}
    return render(request, "base/edit_user.html", context)


def creategroup(request):
    if request.method == "POST":

        name = request.POST.get("name")
        checkbox1 = request.POST.getlist("permission")
        print(checkbox1)
        if name != "":
            if len(Group.objects.filter(name=name)) == 0:
                group = Group(name=name)
                group.save()
                for item in checkbox1:
                    group.permissions.add(item)
                    messages.success(request, "permission was succesfully created")

        return redirect("view-groups")
    context = {}
    return render(request, "base/create_group.html", context)


def add_user_group(request, pk):
    user = User.objects.get(id=pk)
    groups = Group.objects.all()
    ugroup = ""

    if request.method == "POST":
        gname = request.POST.get("group")

        group = Group.objects.get(id=gname)

        user.groups.add(group)

    u_groups = []
    for i in user.groups.all():
        u_groups.append(i)

    context = {"groups": groups, "ugroup": u_groups}

    return render(request, "base/add_user_group.html", context)


def edit_user_to_group(request, pk):
    group = Group.objects.filter(id=pk)
    g_perms = []
    perms = Permission.objects.filter(group__id__in=group)
    for gp in perms:
        g_perms.append(gp.id)
    if request.method == "POST":

        name = request.POST.get("name")
        checkbox1 = request.POST.getlist("permission")
        print(checkbox1)
        # group = Group(name=name)
        # group.save()
        for item in checkbox1:
            group.permissions.add(item)
            messages.success(request, "permission was succesfully updated")

        return redirect("view-groups")
    context = {"g_perms": g_perms, "group": group}

    return render(request, "base/edit_create_to_group.html", context)
