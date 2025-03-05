from django.urls import path
from .views import AddUserView, BulkCreateUsersView

urlpatterns = [
    path('users/add/', AddUserView.as_view(), name='user-create'),
    path('bulk-create-users/', BulkCreateUsersView.as_view(), name='bulk-create-users'),
]
