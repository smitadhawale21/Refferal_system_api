from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token

# @api_view(['POST'])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         token = Token.objects.create(user=user)
#         return Response({'user_id': serializer.data['id'], 'token': token.key, 'message': 'User registered successfully'})
#     return Response(serializer.errors, status=400)
@api_view(['POST'])
def register_user(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    referral_code = request.data.get('referral_code')

    if not name or not email or not password:
        return Response({'message': 'Name, email, and password are required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.User(username=email, email=email, password=password)
    user.first_name = name
    user.save()

    # If referral code is provided, process referral logic here

    # Create token for the user
    token, created = Token.objects.get_or_create(user=user)

    return Response({'user_id': user.id, 'token': token.key, 'message': 'User registered'})


# @api_view(['POST'])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'user_id': serializer.data['id'], 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user  # Retrieve the current authenticated user
    serializer = UserSerializer(user)  
    return Response(serializer.data)

class ReferralsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_referrals(request):
    
    # Get the current user's referral code
    referral_code = request.user.referral_code
    
    # Filter users who registered using the current user's referral code
    referrals = User.objects.filter(referral_code=referral_code)
    
    # Pagination
    paginator = ReferralsPagination()
    result_page = paginator.paginate_queryset(referrals, request)
    
    # Serialize the filtered queryset
    serializer = UserSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)