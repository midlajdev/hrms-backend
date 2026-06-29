from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import SubscriptionPlan
from .serializers import CreateOrderSerializer
from .services.razorpay_service import RazorpayService
from .serializers import VerifyPaymentSerializer
from django.utils import timezone
from .models import UserSubscription
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsEmployer
from apps.payments.permissions import HasActiveSubscription
from apps.ai.services.analytics_service import AnalyticsService
from apps.jobs.models import Job
from apps.payments.models import PaymentTransaction
from apps.users.permissions import IsAdmin
from django.db.models import Sum


class CreateOrderView(APIView):

    def post(self, request):

        try:
            serializer = CreateOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            plan = SubscriptionPlan.objects.get(
                id=serializer.validated_data["plan_id"]
            )

            order = RazorpayService().create_order(plan.price)

            return Response({
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "status": order["status"],
                "key": settings.RAZORPAY_KEY_ID
            })

        except Exception as e:
            return Response(
                {"REAL_ERROR": str(e)},
                status=500
            )
        

class VerifyPaymentView(APIView):

    def post(self, request):

        serializer = VerifyPaymentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:

            RazorpayService().verify_payment(
                **serializer.validated_data
            )

            return Response({
                "message": "Payment verified successfully."
            })

        except Exception:

            return Response(
                {
                    "error": "Payment verification failed."
                },
                status=400
            )
        


class RazorpayWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        event = request.data.get("event")

        print("Webhook Event:", event)

        return Response({
            "message": "Webhook received successfully."
        })
    

class SubscriptionStatusView(APIView):

    permission_classes = [IsAuthenticated]
     
    def get(self, request):

        try:

            subscription = UserSubscription.objects.filter(
                user=request.user,
                status="active",
                end_date__gte=timezone.now().date()
            ).first()

            if not subscription:
                return Response({
                    "active": False
                })

            return Response({
                "active": True,
                "plan": subscription.plan.name,
                "expires_on": subscription.end_date
            })

        except Exception as e:
            return Response(
                {
                    "REAL_ERROR": str(e)
                },
                status=500
            )
        


class PremiumAnalyticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer,
        HasActiveSubscription
    ]

    def get(self, request, job_id):

        try:

            job = Job.objects.get(
                id=job_id,
                employer__user=request.user
            )

        except Job.DoesNotExist:

            return Response(
                {
                    "error":"Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        analytics = AnalyticsService().get_job_analytics(
            job
        )

        return Response(analytics)
    

class TransactionListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        transactions = PaymentTransaction.objects.all().values(
            "transaction_id",
            "amount",
            "payment_method",
            "status",
            "created_at"
        )

        return Response(transactions)
    

class RevenueReportView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        total = PaymentTransaction.objects.filter(
            status="success"
        ).aggregate(
            Sum("amount")
        )["amount__sum"] or 0

        return Response({

            "total_revenue": total,

            "successful_transactions":
                PaymentTransaction.objects.filter(
                    status="success"
                ).count(),

            "failed_transactions":
                PaymentTransaction.objects.filter(
                    status="failed"
                ).count()

        })
    


class RefundLogView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        refunds = PaymentTransaction.objects.filter(
            status="failed"
        ).values(
            "transaction_id",
            "amount",
            "created_at"
        )

        return Response(refunds)