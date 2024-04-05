from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer,CustomTokenObtainPairSerializer
from .models import UserProfile
from django.db.models import Q
import jwt

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if username and password and email:

        try:
            already_exist = User.objects.get(username=username)
            if already_exist:
                return Response("A user with that username or email already exist !!", status=status.HTTP_404_NOT_FOUND) 
        except User.DoesNotExist: 
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(user=user)
                token = CustomTokenObtainPairSerializer.get_token(user=user)
                return Response({'token': str(token), 'user': serializer.data})
            return Response(serializer.errors, status=status.HTTP_200_OK)

    else:
        return Response("Missing required data !!", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response("Username or Password incorrect !!", status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(request.data['password']):
        return Response("Username or Password incorrect !!", status=status.HTTP_404_NOT_FOUND)
    token = CustomTokenObtainPairSerializer.get_token(user=user)
    serializer = UserSerializer(user)
    return Response({'token': str(token), 'user': serializer.data})

@api_view(['POST'])
def refresh_token(request):
    old_token = request.data['token']
    decoded_token = jwt.decode(old_token,algorithms=None,verify=False, options={'verify_signature': False})
    user = get_object_or_404(User, username=decoded_token['username'])
    token = CustomTokenObtainPairSerializer.get_token(user=user)
    return Response({'token': str(token)})
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
