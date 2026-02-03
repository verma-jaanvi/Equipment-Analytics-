from django.urls import path
from .views import UploadCSVView, HistoryView, ReportView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view()), 
    path("upload/", UploadCSVView.as_view()),
    path("history/", HistoryView.as_view()),
    path("report/<int:dataset_id>/", ReportView.as_view()),
]