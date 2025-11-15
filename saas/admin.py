from django.contrib import admin

from .models import (AdvanceDiscount, Agreement, CartItem, Charge, ChargeItem,
                     Coupon, RoleDescription, Plan, Signature, Subscription, Transaction)
from .utils import get_organization_model, get_role_model

Organization = get_organization_model()
Role = get_role_model()

admin.site.register(AdvanceDiscount)
admin.site.register(Agreement)
admin.site.register(CartItem)
admin.site.register(Charge)
admin.site.register(ChargeItem)
admin.site.register(Coupon)
admin.site.register(Organization)
admin.site.register(Plan)
admin.site.register(Role)
admin.site.register(RoleDescription)
admin.site.register(Signature)
admin.site.register(Subscription)
admin.site.register(Transaction)
