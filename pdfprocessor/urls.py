from django.urls import path
from .views import DocumentAnalysisView, index

urlpatterns = [
    path("process/", DocumentAnalysisView.as_view(), name="process-document"),
    path("", index, name="index"),  # Add this line
]
