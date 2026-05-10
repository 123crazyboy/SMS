from django.urls import path

from . import views


app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("students/", views.students, name="students"),
    path("teachers/", views.teachers, name="teachers"),
    path("classes/", views.classes, name="classes"),
    path("subjects/", views.subjects, name="subjects"),
    path("attendance/", views.attendance, name="attendance"),
]
