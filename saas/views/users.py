from django.views.generic import TemplateView

from ..compat import reverse
from ..mixins import UserMixin
from ..utils import update_context_urls


class ProductListView(UserMixin, TemplateView):
    """
    List of organizations a ``:user`` has a role with.

    Template:

    To edit the layout of this page, create a local \
    ``saas/users/roles/index.html`` (`example <https://github.com/djaodjin\
/djaodjin-saas/tree/master/saas/templates/saas/users/roles/index.html>`__).
    You should insure the page will call the
    `/api/users/{user}/accessibles <https://www.djaodjin.com/docs/\
reference/djaoapp/latest/api/#listAccessibleBy>`__
    API end point to fetch the set of organization accessible by the user.

    Template context:
      - ``user`` The organization object users have permissions to.
      - ``request`` The HTTP request object
    """
    template_name = 'saas/users/roles/index.html'

    def get_template_names(self):
        return super(ProductListView, self).get_template_names() + [
            # Implementation note: backward compatibility
            'saas/users/roles.html'
        ]

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        user = self.user

        urls = {
            'api_candidates': reverse('saas_api_search_profiles'),
            'user': {
                'api_accessibles': reverse(
            'saas_api_accessibles', args=(user,)),
                'api_profile_create': reverse(
                    'saas_api_user_profiles', args=(user,)),
            }}
        update_context_urls(context, urls)
        return context
