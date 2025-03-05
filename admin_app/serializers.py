from rest_framework import serializers
from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password','age','location', 'is_active', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data.get('password')
        )
        if 'user_id' in validated_data:
            user.user_id = validated_data['user_id']
        if 'username' in validated_data:
            user.username = validated_data['username']
        if 'email' in validated_data:
            user.email = validated_data['email']
        if 'location' in validated_data:
            user.location = validated_data['location']
        if 'age' in validated_data:
            user.age = validated_data['age']
        user.save()
        return user

class UserBulkCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ['user_id', 'location', 'age']
