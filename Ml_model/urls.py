from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
