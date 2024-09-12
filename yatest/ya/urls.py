from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("download/<path:path>", views.downloadFile, name="downloadFile"),
]