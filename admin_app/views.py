from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserBulkCreateSerializer
import pandas as pd
from django.db import transaction
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAdminUser
import numpy as np

class AddUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class BulkCreateUsersView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if file:
                # Handle CSV file upload
                df = pd.read_csv(file)
                df['Age'] = df['Age'].fillna(value=0)  # Explicitly specify fill value
                df['Location'] = df['Location'].fillna(value='')  # Empty string for location
                
                users_data = []
                skipped_users = []
                existing_user_ids = set(User.objects.values_list('user_id', flat=True))

                with transaction.atomic():
                    for _, row in df.iterrows():
                        user_id = int(row['User-ID']) if 'User-ID' in row else None
                        
                        # Skip if user_id already exists
                        if user_id and user_id in existing_user_ids:
                            skipped_users.append(user_id)
                            continue

                        user_data = {
                            'user_id': user_id,
                            'location': None if row['Location'] == '' else row['Location'],
                            'age': float(row['Age'])
                        }
                        users_data.append(user_data)
            else:
                # Handle JSON data input
                users_data = []
                skipped_users = []
                raw_users_data = request.data.get('users', [])
                existing_user_ids = set(User.objects.values_list('user_id', flat=True))

                for user_data in raw_users_data:
                    user_id = user_data.get('user_id')
                    if user_id and user_id in existing_user_ids:
                        skipped_users.append(user_id)
                        continue
                    users_data.append(user_data)

            if not users_data:
                return Response({
                    'message': 'No new users to create',
                    'skipped_users': skipped_users
                }, status=status.HTTP_200_OK)

            # Validate and create users
            serializer = UserBulkCreateSerializer(data=users_data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': f'Successfully created {len(users_data)} users',
                    'skipped_users': skipped_users,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


