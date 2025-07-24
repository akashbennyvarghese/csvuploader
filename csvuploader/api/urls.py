from django.urls import path
from .views import CSVUploadView, ClearUsersView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('clear-users/', ClearUsersView.as_view(), name='clear-users'),
]
