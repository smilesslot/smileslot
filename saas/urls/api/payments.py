"""
URLs for the payments API of djaodjin saas.
"""

from ...api.charges import PaymentDetailAPIView
from ...compat import path

urlpatterns = [
    path('billing/payments/<slug:claim_code>', PaymentDetailAPIView.as_view(),
        name='saas_api_payment'),
]
