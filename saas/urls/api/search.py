"""
URLs to populate type-ahead candidate lists
"""

from ... import settings
from ...api.accounts import (AccountsTypeaheadAPIView, ProfileAPIView,
    ProfilesTypeaheadAPIView, UsersTypeaheadAPIView)
from ...compat import path


urlpatterns = [
    path('accounts/users',
        UsersTypeaheadAPIView.as_view(), name='saas_api_search_users'),
    path('accounts/profiles/<slug:%s>' %
        settings.PROFILE_URL_KWARG,
        ProfileAPIView.as_view(), name='saas_api_search_profile'),
    path('accounts/profiles',
        ProfilesTypeaheadAPIView.as_view(), name='saas_api_search_profiles'),
    path('accounts',
        AccountsTypeaheadAPIView.as_view(), name='saas_api_search_accounts'),
]
