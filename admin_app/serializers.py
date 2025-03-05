from rest_framework import serializers
from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'is_active', 'created_at']
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data.get('password')
        )
        if 'username' in validated_data:
            user.username = validated_data['username']
        if 'email' in validated_data:
            user.email = validated_data['email']
        user.save()
        return user
