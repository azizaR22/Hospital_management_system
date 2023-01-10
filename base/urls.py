from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexPage, name="index"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("user-registration/", views.user_register, name="user-registration"),
    path("view-doctor/", views.view_doc, name="view-doctor"),
    path("delete-doctor/<str:pk>/", views.delete_doc, name="delete-doctor"),
    path("add-doctor", views.add_doctor, name="add-doctor"),
    path("view-patient", views.view_patient, name="view-patient"),
    path("delete-patient/<str:pk>/", views.delete_patient, name="delete-patient"),
    path("add-patient/", views.addPatient, name="add-patient"),
    path("view_appointments/", views.view_Appoin, name="view-appoinments"),
    path(
        "delete-appoinments/<str:pk>/",
        views.delete_Appoinments,
        name="delete-appointments",
    ),
    path("add-appoinments/", views.add_appoinments, name="add-appointments"),
    path(
        "'update-appointments/<str:pk>/",
        views.updateappointments,
        name="update-appointments",
    ),
    path("update-doctor/<str:pk>/", views.updatedoctor, name="update-doctor"),
    path("update-patient/<str:pk>/", views.updatepatient, name="update-patient"),
    path("view_users/", views.view_users, name="view-users"),
    path("edit-user/", views.adduser, name="add-user"),
    path("view_groups/", views.view_group, name="view-groups"),
    path("delete-userr/<str:pk>/", views.delete_user, name="delete-userr"),
    path("delete-group/<str:pk>/", views.delete_group, name="delete-group"),
    path("add-group/", views.add_group, name="add-group"),
    path("edit-user/<str:pk>", views.edituser, name="edit-user"),
    path("create-group/", views.creategroup, name="create-group"),
    path("add-user-to-group/", views.add_user_group, name="add-user-to-group"),
    path("edit-user-to-group/", views.edit_user_to_group, name="edit-user-to-group"),
]
