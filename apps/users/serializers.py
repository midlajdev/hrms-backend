import os
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import CandidateProfile, EmployerProfile, AdminActionLog

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role

        return data
    
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'role']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class CandidateProfileSerializer(serializers.ModelSerializer):

    resume = serializers.FileField(read_only=True)
    class Meta:
        model = CandidateProfile
        fields = "__all__"
        read_only_fields = ("user", "is_active", "created_at", "updated_at")

    def validate(self, data):
        for field in ["expected_salary", "current_salary"]:
            value = data.get(field)
            if value is not None and value <= 0:
                raise serializers.ValidationError(
                    {field: "Salary must be greater than 0"}
                )
        return data

    def validate_total_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experiance must be greater than 0")
        return value
    
class EmployerProfileSerializer(serializers.ModelSerializer):
    is_flagged = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = EmployerProfile
        fields = "__all__"
        read_only_fields = ("user", "is_verified", "is_active", "created_at", "updated_at")

    def get_is_flagged(self, obj):
        return obj.user.is_flagged

    def get_flag_count(self, obj):
        return obj.user.flag_count

    def get_email(self, obj):
        return obj.user.email

    def validate_founded_year(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value and value > current_year:
            raise serializers.ValidationError("Founded year cannot be in the future.")
        return value
    
class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ['resume']

    def validate_resume(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("File size must be under 2MB.")

        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf','.docx']

        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError("Only PDF, DOC, DOCX allowed.")
        
        allowed_mime_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]

        if value.content_type not in allowed_mime_types:
            raise serializers.ValidationError(
                "Invalid file type."
            )
        return value
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CandidateListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CandidateProfile
        fields = "__all__"

class FlaggedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'is_flagged',
            'flag_count',
            'is_active'
        ]

class AdminActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActionLog
        fields = "__all__"