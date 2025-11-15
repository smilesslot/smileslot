"""
URLs API for profile resources (managers, custom roles and subscriptions)
"""

from .... import settings
from ....api.organizations import (
    OrganizationDetailAPIView, OrganizationPictureAPIView)
from ....api.subscriptions import (ExpiredSubscriptionsAPIView,
    SubscriptionDetailAPIView, SubscribedSubscriptionListAPIView)
from ....compat import path


urlpatterns = [
    path('profile/<slug:%s>/subscriptions/expired' %
        settings.PROFILE_URL_KWARG,
        ExpiredSubscriptionsAPIView.as_view(),
        name='saas_api_subscriptions_expired'),
    path('profile/<slug:%s>/subscriptions/<slug:subscribed_plan>' %
        settings.PROFILE_URL_KWARG,
        SubscriptionDetailAPIView.as_view(),
        name='saas_api_subscription_detail'),
    path('profile/<slug:%s>/subscriptions' %
        settings.PROFILE_URL_KWARG,
        SubscribedSubscriptionListAPIView.as_view(),
        name='saas_api_subscription_list'),
    path('profile/<slug:%s>/picture' %
        settings.PROFILE_URL_KWARG,
        OrganizationPictureAPIView.as_view(),
        name='saas_api_organization_picture'),
    path('profile/<slug:%s>' %
        settings.PROFILE_URL_KWARG,
        OrganizationDetailAPIView.as_view(), name='saas_api_organization'),
]
