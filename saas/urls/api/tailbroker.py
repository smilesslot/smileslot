"""
URLs for API available typically only to the broker platform and
that must be included after the provider and subscriber urls.
"""

from ... import settings
from ...api.organizations import OrganizationListAPIView
from ...api.renewals import RenewalsAPIView
from ...compat import path


urlpatterns = [
    path('billing/<slug:%s>/renew' %
        settings.PROFILE_URL_KWARG,
        RenewalsAPIView.as_view(), name='saas_api_renewals'),
    path('profile',
        OrganizationListAPIView.as_view(),
        name='saas_api_profile'),
]
