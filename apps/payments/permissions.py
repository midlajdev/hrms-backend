from rest_framework.permissions import BasePermission
from django.utils import timezone

from apps.payments.models import UserSubscription


class HasActiveSubscription(BasePermission):

    message = "Active subscription required."

    def has_permission(self, request, view):

        return UserSubscription.objects.filter(
            user=request.user,
            status="active",
            end_date__gte=timezone.now().date()
        ).exists()