"""
API URLs for a provider plans
"""

from .... import settings
from ....api.plans import (PlanListCreateAPIView, PlanDetailAPIView)
from ....compat import path


urlpatterns = [
    path('profile/<slug:%s>/plans/<slug:plan>' %
        settings.PROFILE_URL_KWARG,
        PlanDetailAPIView.as_view(), name='saas_api_plan'),
    path('profile/<slug:%s>/plans' %
        settings.PROFILE_URL_KWARG,
        PlanListCreateAPIView.as_view(), name='saas_api_plans'),
]
