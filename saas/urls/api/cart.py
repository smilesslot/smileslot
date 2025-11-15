"""
URLs for the cart API of djaodjin saas.
"""

from ...api.agreements import AgreementDetailAPIView, AgreementListAPIView
from ...api.billing import (CartItemAPIView, CartItemUploadAPIView,
                            CouponRedeemAPIView)
from ...api.plans import PricingAPIView
from ...compat import path

urlpatterns = [
    path('pricing',
        PricingAPIView.as_view(), name='saas_api_pricing'),
    path('cart/redeem',
        CouponRedeemAPIView.as_view(), name='saas_api_redeem_coupon'),
    path('cart/<slug:plan>/upload',
        CartItemUploadAPIView.as_view(), name='saas_api_cart_upload'),
    path('cart', CartItemAPIView.as_view(), name='saas_api_cart'),
    path('legal/<slug:agreement>', AgreementDetailAPIView.as_view(),
        name='saas_api_legal_detail'),
    path('legal', AgreementListAPIView.as_view(), name='saas_api_legal'),
]
