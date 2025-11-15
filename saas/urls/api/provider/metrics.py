"""
URLs API for provider resources related to billing
"""

from .... import settings
from ....api.federations import (FederatedSubscribersAPIView,
    SharedProfilesAPIView)
from ....api.metrics import (BalancesAPIView, CouponUsesAPIView,
    CustomerMetricAPIView, LifetimeValueMetricAPIView, PlanMetricAPIView,
    RevenueMetricAPIView, BalancesDueAPIView)
from ....compat import path


urlpatterns = [
    path('metrics/<slug:%s>/coupons/<slug:coupon>' %
        settings.PROFILE_URL_KWARG,
        CouponUsesAPIView.as_view(), name='saas_api_coupon_uses'),
    path('metrics/<slug:%s>/balances' %
        settings.PROFILE_URL_KWARG,
        BalancesAPIView.as_view(), name='saas_api_balances'),
    path('metrics/<slug:%s>/customers' %
        settings.PROFILE_URL_KWARG,
        CustomerMetricAPIView.as_view(), name='saas_api_customer'),
    path('metrics/<slug:%s>/plans' %
        settings.PROFILE_URL_KWARG,
        PlanMetricAPIView.as_view(), name='saas_api_metrics_plans'),
    path('metrics/<slug:%s>/funds' %
        settings.PROFILE_URL_KWARG,
        RevenueMetricAPIView.as_view(), name='saas_api_revenue'),
    path('metrics/<slug:%s>/lifetimevalue' %
        settings.PROFILE_URL_KWARG,
        LifetimeValueMetricAPIView.as_view(),
        name='saas_api_metrics_lifetimevalue'),
    path('metrics/<slug:%s>/balances-due' %
         settings.PROFILE_URL_KWARG,
         BalancesDueAPIView.as_view(),
         name='saas_api_metrics_balances_due'),

    # Metrics for a federation of providers
    path('metrics/<slug:%s>/federated/shared' %
        settings.PROFILE_URL_KWARG,
        SharedProfilesAPIView.as_view(),
        name="saas_api_shared_profiles"),
    path('metrics/<slug:%s>/federated' %
        settings.PROFILE_URL_KWARG,
        FederatedSubscribersAPIView.as_view(),
        name="saas_api_federated_subscribers")
]
