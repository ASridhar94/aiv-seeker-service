from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.submit_workflow, name="submit_workflow"),
    path("submitted/<int:workflow_id>", views.submitted, name="submitted"),
    path("show/<int:workflow_id>", views.show_workflow, name="show_workflow"),
    path("", views.index, name="index"),
]
