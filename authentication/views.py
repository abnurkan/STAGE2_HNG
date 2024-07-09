from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from django.shortcuts import get_object_or_404
from .models import User


# 1. Register User with default Organisation
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)



#2.  Login  user Endpoint
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": {
                        "userId": str(user.userId),
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone
                    }
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)



#3 fetched user info 
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(User, id=id)
        if user == request.user or user.organisations.filter(users=request.user).exists():
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Forbidden",
            "message": "You do not have permission to access this user",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)



#4 user can get all organisation he belons to  

        return Organisation.objects.filter(users=user)


# 4 user can get all organisation he belons to   and can create new organisation
class Organisations(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        organisations = Organisation.objects.filter(users=user)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
     #user can create new organisation
    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                "status": "success",
                "message": "Organisation created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)

     
#5 login user get single organisation record

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orgId, *args, **kwargs):
        organisation = get_object_or_404(Organisation, id=orgId)
        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    
6. #added user to a particularorganisation
class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId, *args, **kwargs):
        organisation = get_object_or_404(Organisation, id=orgId)
        userId = request.data.get('userId')
        user = get_object_or_404(User, id= userId)
        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully",
        }, status=status.HTTP_200_OK)
    
