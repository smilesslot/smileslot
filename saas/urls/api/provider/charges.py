"""
URLs API for charges that can only be accessed by a provider.
"""

from .... import settings
from ....api.charges import ChargeRefundAPIView, PaymentCollectedAPIView
from ....compat import path

# Actually a <charge> slug. We are using <organization> here such that
# it plays nice with the rules-based permission checks.
urlpatterns = [
    path('billing/<slug:%s>/payments/<slug:claim_code>/collected' %
        settings.PROFILE_URL_KWARG,
        PaymentCollectedAPIView.as_view(), name='saas_api_payment_collected'),
    path('billing/<slug:%s>/charges/<slug:charge>/refund' %
        settings.PROFILE_URL_KWARG,
        ChargeRefundAPIView.as_view(), name='saas_api_charge_refund'),
]
