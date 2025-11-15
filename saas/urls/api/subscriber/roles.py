"""
URLs API for profile managers and custom roles on an Organization
"""

from .... import settings
from ....api.roles import (RoleListAPIView, RoleByDescrListAPIView,
    RoleDetailAPIView)
from ....compat import path, re_path


urlpatterns = [
    re_path(r'profile/(?P<%s>%s)/roles/(?P<role>%s)/(?P<user>%s)' % (
        settings.PROFILE_URL_KWARG, settings.SLUG_RE,
        settings.SLUG_RE, settings.MAYBE_EMAIL_REGEX),
        RoleDetailAPIView.as_view(), name='saas_api_role_detail'),
    path('profile/<slug:%s>/roles/<slug:role>' %
        settings.PROFILE_URL_KWARG,
        RoleByDescrListAPIView.as_view(),
        name='saas_api_roles_by_descr'),
    path('profile/<slug:%s>/roles' %
        settings.PROFILE_URL_KWARG,
        RoleListAPIView.as_view(), name='saas_api_roles'),
]
