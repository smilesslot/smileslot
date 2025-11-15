import logging

from django.db.models import F, Min, Max

from ..models import Subscription


LOGGER = logging.getLogger(__name__)


def active_subscribers_by_period(plan, date_periods=None):
    """
    List of active subscribers for a *plan* for a certain time period.
    """
    if date_periods is None:
        date_periods = []

    values = []
    for end_period in date_periods:
        values.append([end_period,
            Subscription.objects.active_at(end_period, plan=plan).count()])

    return values


def churn_subscribers_by_period(plan=None, date_periods=None):
    """
    List of churn subscribers from the previous period for a *plan*
    for specific time periods.
    """
    if date_periods is None:
        date_periods = []

    kwargs = {}
    if plan:
        kwargs = {'plan': plan}

    values = []
    start_period = date_periods[0]
    for end_period in date_periods[1:]:
        values.append([end_period, Subscription.objects.churn_in_period(
            start_period, end_period, **kwargs).count()])
        start_period = end_period

    return values


def subscribers_age(provider=None):
    if provider:
        queryset = Subscription.objects.filter(plan__organization=provider)
    else:
        queryset = Subscription.objects.all()
    return queryset.values(slug=F('organization__slug')).annotate(
        created_at=Min('created_at'), ends_at=Max('ends_at')).order_by(
        'organization__slug')
