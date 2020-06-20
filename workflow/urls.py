from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.submit_workflow, name="submit_workflow"),
    path("", views.index, name="index"),
]
