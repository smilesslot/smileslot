"""
URLs for API related to signing legal agreements.
"""

from ...api.users import AgreementSignAPIView
from ...compat import path


urlpatterns = [
    path('legal/<slug:agreement>/sign',
        AgreementSignAPIView.as_view(), name='saas_api_sign_agreement')
]
