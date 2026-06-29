from django.contrib import admin
from apps.payments.models import BillingHistory,SubscriptionPlan,PaymentTransaction,UserSubscription
# Register your models here.
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(PaymentTransaction)
admin.site.register(BillingHistory)