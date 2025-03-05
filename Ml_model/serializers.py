from rest_framework import serializers
from .models import Book, Rating
from admin_app.models import User
from admin_app.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user_id', read_only=True)
    book_details = BookSerializer(source='book_isbn', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user_id', 'book_isbn', 'rating', 'user_details', 'book_details']

