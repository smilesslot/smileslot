"""
URLs API for resources
"""

from .... import settings
from ....api.charges import ChargeResourceView, EmailChargeReceiptAPIView
from ....compat import path


urlpatterns = [
    path('billing/<slug:%s>/charges/<slug:charge>/email' %
        settings.PROFILE_URL_KWARG,
        EmailChargeReceiptAPIView.as_view(),
        name='saas_api_email_charge_receipt'),
    path('billing/<slug:%s>/charges/<slug:charge>' %
        settings.PROFILE_URL_KWARG,
        ChargeResourceView.as_view(), name='saas_api_charge'),
]
