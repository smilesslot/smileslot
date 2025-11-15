"""
URLs for backends of saas Django app
"""

from ...compat import include, re_path

urlpatterns = [
    re_path(r'^', include('saas.backends.stripe_processor.urls.api')),
]
