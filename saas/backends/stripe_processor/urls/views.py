from ..views import StripeProcessorRedirectView
from ....compat import re_path


urlpatterns = [
    re_path(r'^stripe/billing/connected/',
        StripeProcessorRedirectView.as_view(
            pattern_name='saas_update_bank'),
        name='saas_processor_connected_hook'),
]
