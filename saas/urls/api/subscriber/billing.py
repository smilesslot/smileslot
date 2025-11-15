"""
URLs billing API for subscribers
"""

from .... import settings
from ....api.billing import CheckoutAPIView, PaylaterAPIView
from ....api.backend import PaymentMethodDetailAPIView
from ....api.transactions import BillingsAPIView, StatementBalanceAPIView
from ....compat import path


urlpatterns = [
    path('billing/<slug:%s>/balance' %
        settings.PROFILE_URL_KWARG,
        StatementBalanceAPIView.as_view(), name='saas_api_cancel_balance_due'),
    path('billing/<slug:%s>/history' %
        settings.PROFILE_URL_KWARG,
        BillingsAPIView.as_view(), name='saas_api_billings'),
    path('billing/<slug:%s>/card' %
        settings.PROFILE_URL_KWARG,
        PaymentMethodDetailAPIView.as_view(), name='saas_api_card'),
    path('billing/<slug:%s>/checkout/paylater' %
        settings.PROFILE_URL_KWARG,
        PaylaterAPIView.as_view(), name='saas_api_paylater'),
    path('billing/<slug:%s>/checkout' %
        settings.PROFILE_URL_KWARG,
        CheckoutAPIView.as_view(), name='saas_api_checkout'),
]
