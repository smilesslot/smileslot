"""
API URLs for a provider custom roles
"""

from .... import settings
from ....api.roles import (RoleDescriptionListCreateView,
    RoleDescriptionDetailView)
from ....compat import path


urlpatterns = [
    path(r'profile/<slug:%s>/roles/describe/<slug:role>' %
        settings.PROFILE_URL_KWARG,
        RoleDescriptionDetailView.as_view(),
        name='saas_api_role_description_detail'),
    path(r'profile/<slug:%s>/roles/describe' %
        settings.PROFILE_URL_KWARG,
        RoleDescriptionListCreateView.as_view(),
        name='saas_api_role_description_list'),
]
