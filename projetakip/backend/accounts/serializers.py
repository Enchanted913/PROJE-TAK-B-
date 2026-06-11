from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    display_role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'display_role', 'student_number', 'phone',
        )
        read_only_fields = ('role',)


class StudentWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'student_number', 'phone', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', 'ogrenci123')
        user = User(**validated_data, role=User.Role.STUDENT)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'student_number', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Şifreler eşleşmiyor.'})
        if data['role'] not in (User.Role.TEACHER, User.Role.STUDENT):
            raise serializers.ValidationError({'role': 'Geçersiz rol.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Kullanıcı adı veya şifre hatalı.')
        if not user.is_active:
            raise serializers.ValidationError('Hesap pasif.')
        data['user'] = user
        return data
