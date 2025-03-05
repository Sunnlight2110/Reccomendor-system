from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Rating
from .serializers import BookSerializer, RatingSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

