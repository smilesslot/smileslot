
from ..views import StripeWebhook
from ....settings import PROCESSOR_HOOK_URL
from ....compat import re_path

urlpatterns = [
    re_path(r'^%s' % PROCESSOR_HOOK_URL,
        StripeWebhook.as_view(), name='saas_processor_hook')
]
