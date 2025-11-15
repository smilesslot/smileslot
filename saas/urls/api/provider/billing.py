"""
URLs API for provider resources related to billing
"""

from .... import settings
from ....api.backend import RetrieveBankAPIView
from ....api.coupons import CouponListCreateAPIView, CouponDetailAPIView
from ....api.transactions import ReceivablesListAPIView, TransferListAPIView
from ....compat import path

urlpatterns = [
    path('billing/<slug:%s>/bank' %
        settings.PROFILE_URL_KWARG,
        RetrieveBankAPIView.as_view(), name='saas_api_bank'),
    path('billing/<slug:%s>/coupons/<slug:coupon>' %
        settings.PROFILE_URL_KWARG,
        CouponDetailAPIView.as_view(), name='saas_api_coupon_detail'),
    path('billing/<slug:%s>/coupons' %
        settings.PROFILE_URL_KWARG,
        CouponListCreateAPIView.as_view(), name='saas_api_coupon_list'),
    path('billing/<slug:%s>/receivables' %
        settings.PROFILE_URL_KWARG,
        ReceivablesListAPIView.as_view(), name='saas_api_receivables'),
    path('billing/<slug:%s>/transfers' %
        settings.PROFILE_URL_KWARG,
        TransferListAPIView.as_view(), name='saas_api_transfer_list'),
]
