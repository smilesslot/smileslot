"""
API URLs for a provider subcribers.
"""

from .... import settings
from ....api.organizations import (ActiveSubscribersAPIView,
    EngagedSubscribersAPIView, ProviderAccessiblesAPIView,
    UnengagedSubscribersAPIView)
from ....api.subscriptions import (ActiveSubscriberSubscriptionsAPIView,
    AllSubscriberSubscriptionsAPIView, ChurnedSubscribersAPIView,
    PlanAllSubscribersAPIView,
    PlanActiveSubscribersAPIView, PlanChurnedSubscribersAPIView,
    PlanSubscriptionDetailAPIView, SubscriptionRequestAcceptAPIView)
from ....compat import path, re_path


urlpatterns = [
    re_path(r'profile/(?P<%s>%s)/subscribers/accept/(?P<request_key>%s)' % (
        settings.PROFILE_URL_KWARG, settings.SLUG_RE,
        settings.VERIFICATION_KEY_RE),
        SubscriptionRequestAcceptAPIView.as_view(),
        name='saas_api_subscription_grant_accept'),
    path('profile/<slug:%s>/subscribers/subscriptions/all' %
        settings.PROFILE_URL_KWARG,
        AllSubscriberSubscriptionsAPIView.as_view(),
        name='saas_api_subscribed_and_churned'),
    path('profile/<slug:%s>/subscribers/subscriptions/churned' %
        settings.PROFILE_URL_KWARG,
        ChurnedSubscribersAPIView.as_view(),
        name='saas_api_churned'),
    path('profile/<slug:%s>/subscribers/subscriptions' %
        settings.PROFILE_URL_KWARG,
        ActiveSubscriberSubscriptionsAPIView.as_view(),
        name='saas_api_subscribed'),

    path('profile/<slug:%s>/subscribers/engaged' %
        settings.PROFILE_URL_KWARG,
        EngagedSubscribersAPIView.as_view(),
        name='saas_api_engaged_subscribers'),
    path('profile/<slug:%s>/subscribers/unengaged' %
        settings.PROFILE_URL_KWARG,
        UnengagedSubscribersAPIView.as_view(),
        name='saas_api_unengaged_subscribers'),
    path('profile/<slug:%s>/subscribers/all' %
        settings.PROFILE_URL_KWARG,
        ProviderAccessiblesAPIView.as_view(), name='saas_api_subscribers_all'),
    path('profile/<slug:%s>/subscribers' %
        settings.PROFILE_URL_KWARG,
        ActiveSubscribersAPIView.as_view(), name='saas_api_subscribers'),

    path('profile/<slug:%s>/plans/<slug:plan>/subscriptions/all' %
        settings.PROFILE_URL_KWARG,
        PlanAllSubscribersAPIView.as_view(),
        name='saas_api_plan_subscribers_all'),
    path('profile/<slug:%s>/plans/<slug:plan>/subscriptions/churned' %
        settings.PROFILE_URL_KWARG,
        PlanChurnedSubscribersAPIView.as_view(),
        name='saas_api_plan_subscribers_churned'),
    path(
    'profile/<slug:%s>/plans/<slug:plan>/subscriptions/<slug:subscriber>' %
        settings.PROFILE_URL_KWARG,
        PlanSubscriptionDetailAPIView.as_view(),
        name='saas_api_plan_subscription'),
    path('profile/<slug:%s>/plans/<slug:plan>/subscriptions' %
        settings.PROFILE_URL_KWARG,
        PlanActiveSubscribersAPIView.as_view(),
        name='saas_api_plan_subscribers'),
]
