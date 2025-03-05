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
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Read CSV file
            df = pd.read_csv(file)

            # Handle missing values
            df['Age'] = df['Age'].fillna(0)
            df['Location'] = df['Location'].fillna(None)
            
            # Prepare data for bulk create
            users_data = []
            with transaction.atomic():
                for _, row in df.iterrows():
                    user_data = {
                        'user_id': int(row['User-ID']),
                        'location': row['Location'] if pd.notna(row['Location']) else None,
                        'age': float(row['Age']) if pd.notna(row['Age']) else 0
                    }
                    users_data.append(user_data)

                # Validate and create users
                serializer = UserBulkCreateSerializer(data=users_data, many=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'message': f'Successfully created {len(users_data)} users',
                        'data': serializer.data
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


