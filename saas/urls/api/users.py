"""
URLs for API related to users accessible by.
"""

from ... import settings
from ...api.roles import (AccessibleByListAPIView, AccessibleDetailAPIView,
                          RoleAcceptAPIView, AccessibleByDescrListAPIView, UserProfileListAPIView,
                          )
from ...compat import path, re_path

urlpatterns = [
    re_path(
        r'^users/(?P<user>%s)/accessibles/accept/(?P<verification_key>%s)' % (
        settings.SLUG_RE, settings.VERIFICATION_KEY_RE),
        RoleAcceptAPIView.as_view(), name='saas_api_accessibles_accept'),
    path('users/<slug:user>/accessibles/<slug:role>/<slug:%s>' %
        settings.PROFILE_URL_KWARG,
        AccessibleDetailAPIView.as_view(), name='saas_api_accessible_detail'),
    path('users/<slug:user>/accessibles/<slug:role>',
        AccessibleByDescrListAPIView.as_view(),
        name='saas_api_accessibles_by_descr'),
    path('users/<slug:user>/accessibles',
        AccessibleByListAPIView.as_view(), name='saas_api_accessibles'),
    path('users/<slug:user>/profiles',
        UserProfileListAPIView.as_view(), name='saas_api_user_profiles'),
]
