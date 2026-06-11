from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsTeacher

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, StudentWriteSerializer, UserSerializer


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FCMTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('fcm_token', '')
        request.user.fcm_token = token
        request.user.save(update_fields=['fcm_token'])
        return Response({'detail': 'FCM token kaydedildi.'})


class StudentListCreateAPIView(generics.ListCreateAPIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsTeacher()]

    def get_queryset(self):
        return User.objects.filter(role=User.Role.STUDENT).order_by('last_name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentWriteSerializer
        return UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    queryset = User.objects.filter(role=User.Role.STUDENT)
    serializer_class = StudentWriteSerializer
