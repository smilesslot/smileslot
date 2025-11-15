import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rules.urldecorators import include, re_path # because we want to use
                                                # `fail_` decorators redirects.
from saas import settings as saas_settings
from saas.compat import reverse_lazy
from saas.decorators import (fail_active_roles, fail_agreement,
    fail_authenticated, fail_direct, fail_provider, fail_provider_only,
    fail_self_provider)
from saas.views import OrganizationRedirectView, UserRedirectView

from . import signals #pylint:disable=unused-import
from .views.app import AppView
from .views.organization import OrganizationListView, UserProfileView


admin.autodiscover()


def url_prefixed(regex, view, name=None, redirects=None):
    """
    Returns a urlpattern for public pages.
    """
    return re_path(r'^' + regex, view, name=name, redirects=redirects)


# admin doc and panel
try:
    urlpatterns = [
        re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ]
except ImproperlyConfigured: # Django <= 1.9
    urlpatterns = [
        re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    re_path(r'^__debug__/', include(debug_toolbar.urls)),
    url_prefixed(r'', include('saas.urls.views.request'),
        redirects=[fail_authenticated]),
    url_prefixed(r'', include('saas.urls.views.users'),
        redirects=[fail_authenticated]),
    url_prefixed(r'users/(?P<user>[\w.@+-]+)/',
        UserProfileView.as_view(), name='users_profile',
        redirects=[fail_authenticated]),
    url_prefixed(r'users/',
        UserRedirectView.as_view(), name='accounts_profile',
        redirects=[fail_authenticated]),
    url_prefixed(r'', include('django.contrib.auth.urls')),
    url_prefixed(r'saas/$',
        OrganizationListView.as_view(), name='saas_organization_list',
        redirects=[fail_authenticated]),
    url_prefixed(r'$', TemplateView.as_view(template_name='billings/index.html'),
        name='home'),
    url_prefixed(r'billing/cart/',
        login_required(
            OrganizationRedirectView.as_view(
                pattern_name='saas_organization_cart'),
            login_url=reverse_lazy('registration_register')),
        name='saas_cart'),
    # saas urls with provider key to implement marketplace.
    url_prefixed(r'api/', include('saas.backends.urls.api')),
    url_prefixed(r'api/', include('saas.urls.api.cart')),
    url_prefixed(r'api/', include('saas.urls.api.payments')),
    url_prefixed(r'api/', include('saas.urls.api.legal'),
        redirects=[fail_authenticated]),
    url_prefixed(r'api/', include('saas.urls.api.search'),
        redirects=[fail_authenticated]),
    url_prefixed(r'api/', include('saas.urls.api.users'),
        redirects=[fail_authenticated, fail_self_provider]),
    url_prefixed(r'api/', include('saas.urls.api.headbroker'),
        redirects=[fail_authenticated, fail_provider_only]),
    # api/charges/:charge/refund must be before api/charges/
    url_prefixed(r'api/',
        include('saas.urls.api.provider.charges'),
        redirects=[fail_authenticated, fail_provider_only]),
    url_prefixed(r'api/',
        include('saas.urls.api.provider.billing'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'api/',
        include('saas.urls.api.provider.roles'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'api/',
        include('saas.urls.api.provider.subscribers'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'api/',
        include('saas.urls.api.provider.plans'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'api/',
        include('saas.urls.api.provider.metrics'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'api/', include('saas.urls.api.subscriber'),
        redirects=[fail_authenticated, fail_provider]),
    url_prefixed(r'api/', include('saas.urls.api.tailbroker'),
        redirects=[fail_authenticated, fail_provider_only]),
    # views
    url_prefixed(r'', include('saas.urls.views.request'), redirects=[fail_authenticated]),
    url_prefixed(r'', include('saas.urls.views.noauth')),
    url_prefixed(r'', include('saas.urls.views.payments')),
    url_prefixed(r'', include('saas.urls.views.headredirects'),
        redirects=[fail_authenticated]),
    url_prefixed(r'', include('saas.urls.views.broker'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'', include('saas.urls.views.provider'),
        redirects=[fail_authenticated, fail_direct]),
    url_prefixed(r'', include('saas.urls.views.subscriber'),
        redirects=[fail_authenticated, fail_agreement, fail_active_roles,
            fail_provider]),
    url_prefixed(r'', include('saas.urls.views.tailredirects'),
        redirects=[fail_authenticated]),

    url_prefixed(r'', include('saas.backends.urls.views')),
    url_prefixed(r'app/(?P<%s>%s)/' % (
        saas_settings.PROFILE_URL_KWARG, saas_settings.SLUG_RE),
        AppView.as_view(template_name='app.html'), name='app',
        redirects=[fail_authenticated]),
    url_prefixed(r'app/',
        OrganizationRedirectView.as_view(), name='product_default_start',
        redirects=[fail_authenticated]),
]
