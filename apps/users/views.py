from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .serializers import CustomTokenObtainPairSerializer, SignupSerializer, CandidateProfileSerializer, EmployerProfileSerializer,ResumeUploadSerializer, UserListSerializer, CandidateListSerializer, FlaggedUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.users.permissions import IsCandidate, IsEmployer, IsAdmin
from .models import CandidateProfile, EmployerProfile, AdminActionLog
from apps.users.serializers import AdminActionLogSerializer
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from utils.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from services.auth_service import generate_tokens, logout_user
from utils.adminLog import log_admin_action

User = get_user_model()

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = generate_tokens(user)

        return Response({
            "success": True,
            "data": serializer.data,
            "message": "User created successfully",
            "access": tokens["access"],
            "refresh": tokens["refresh"]
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=400)

            logout_user(refresh_token)
            
            return Response({
            "success": True,
            "message": "Logged out successfully"
        }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)
        

class candidateProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CandidateProfile.objects.get(user=self.request.user)
    
class CandidateProfilesoftDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CandidateProfile.objects.get(user=self.request.user)
    
    def perform_destroy(self, instance):
        if not instance.is_active:
            raise ValidationError("Profile already deleted")
        # deactivate profile
        instance.is_active = False
        instance.save()
        # deactivate user account
        user = self.request.user
        user.is_active = False
        user.save()
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "success": True,
            "message": "Account deleted successfully"
        }, status=200)

#Employer profile view:
class EmployerProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_object(self):
        try:
            profile = self.request.user.employer_profile
            if not profile.is_active:
                raise NotFound("Profile is inactive.")
            return profile
        except EmployerProfile.DoesNotExist:
            raise NotFound("Employer profile not found.")

class EmployerProfileSoftDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.employer_profile

    def perform_destroy(self, instance):
        if not instance.is_active:
            raise ValidationError("Profile already deleted.")
        instance.is_active = False
        instance.save()

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        candidate = request.user.candidate_profile

        if candidate.resume:
            candidate.resume.delete(save=False)
        serializer = ResumeUploadSerializer(
            candidate,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Resume uploaded successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=400)
    

class AllUserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CustomPagination
    filterset_fields = ["is_active", "created_at","role"]
    
class CandidateListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    # queryset = CandidateProfile.objects.all()
    queryset = CandidateProfile.objects.select_related("user")
    serializer_class = CandidateListSerializer
    pagination_class = CustomPagination
    
    filterset_fields = ["is_active", "created_at"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["skills","location"]

# for admin approval
class ApproveEmployerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, employer_id):
        employer = EmployerProfile.objects.get(id=employer_id)
        employer.is_approved = True
        employer.save()
        log_admin_action(
                admin=request.user,
                action="Approved Employer",
                target_type="Employer",
                target_id=employer.id,
            )
        return Response({"message": "Employer approved"})


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        log_admin_action(
                admin=request.user,
                action="Blocked user",
                target_type="User",
                target_id=user.id,
            )
        return Response({"message": "User blocked"})

class FlagUserView(APIView):

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_flagged = True
        user.flag_count += 1
        user.save()
        return Response({"message": "User flagged for review"})
    
class FlaggedUsersListView(generics.ListAPIView):
    queryset = User.objects.filter(is_flagged=True)
    serializer_class = FlaggedUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class HandleFlaggedUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        action = request.data.get("action")
        if action == "block":
            user.is_active = False
            user.save()

            log_admin_action(
                admin=request.user,
                action="user blocked",
                target_type="user",
                target_id=user.id,
            )
        elif action == "clear":
            user.is_flagged = False
            user.flag_count = 0
            user.save()

            log_admin_action(
                admin=request.user,
                action="Cleared user flag",
                target_type="user",
                target_id=user.id,
            )
        
        else:
            return Response({"error": "Invalid action"}, status=400)

        return Response({"message": f"User {action} successful"})
    

class AdminLogsView(generics.ListAPIView):
    queryset = AdminActionLog.objects.all().order_by('-created_at')
    serializer_class = AdminActionLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]