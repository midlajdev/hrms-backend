import razorpay
from django.conf import settings


class RazorpayService:

    def __init__(self):
        self.client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

    def create_order(self, amount):

        data = {
            "amount": int(amount * 100),   # Razorpay expects paise
            "currency": "INR",
            "payment_capture": 1
        }

        return self.client.order.create(data=data)
    
    def verify_payment(
        self,
        razorpay_order_id,
        razorpay_payment_id,
        razorpay_signature
    ):

        params = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        self.client.utility.verify_payment_signature(params)

        return True