from django.db import models

# Create your models here.
from apps.users.models import User


class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=50)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration_days = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"


class PaymentTransaction(models.Model):

    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
        ("pending", "Pending"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.transaction_id


class BillingHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    billed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number