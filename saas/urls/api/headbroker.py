"""
URLs API for resources available typically only to the broker platform.
"""

from ...api.agreements import AgreementListCreateAPIView, AgreementUpdateAPIView
from ...api.balances import (BalanceLineListAPIView, BrokerBalancesAPIView,
    BalanceLineDetailAPIView)
from ...api.billing import (UserCartItemListView, ActiveCartItemListCreateView,
                            ActiveCartItemRetrieveUpdateDestroyView)
from ...api.charges import ChargeListAPIView
from ...api.transactions import TransactionListAPIView
from ...api.users import RegisteredAPIView
from ...compat import path


urlpatterns = [
    path('agreements/<slug:document>',# We use `document`, not `agreement` here
         # to avoid the `fail_agreement` decorator to send us a curve ball
         # asking to sign a document we just uploaded.
        AgreementUpdateAPIView.as_view(), name='saas_api_agreement_detail'),
    path('agreements',
        AgreementListCreateAPIView.as_view(), name='saas_api_agreements'),
    path('billing/transactions',
        TransactionListAPIView.as_view(), name='saas_api_transactions'),
    path('billing/charges', ChargeListAPIView.as_view(),
        name='saas_api_charges'),
    path('billing/cartitems/user/<slug:user>',
        UserCartItemListView.as_view(), name='saas_api_user_cartitems'),
    path('billing/cartitems/<int:cartitem_id>',
        ActiveCartItemRetrieveUpdateDestroyView.as_view(),
        name='saas_api_cartitems_detail'),
    path('billing/cartitems',
        ActiveCartItemListCreateView.as_view(), name='saas_api_cartitems'),
    path('metrics/balances/<slug:report>/lines/<int:rank>',
        BalanceLineDetailAPIView.as_view(), name='saas_api_balance_line'),
    path('metrics/balances/<slug:report>/lines',
        BalanceLineListAPIView.as_view(), name='saas_api_balance_lines'),
    path('metrics/balances/<slug:report>',
        BrokerBalancesAPIView.as_view(), name='saas_api_broker_balances'),
    path('metrics/registered',
        RegisteredAPIView.as_view(), name='saas_api_registered'),
]
