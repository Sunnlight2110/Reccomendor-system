from django.urls import path
from .views import AddUserView

urlpatterns = [
    path('users/add/', AddUserView.as_view(), name='user-create'),
]
