from django.conf import settings

def js_framework(request):#pylint:disable=unused-argument
    return {
        'USE_STRIPE_V2': settings.USE_STRIPE_V2,
        'DATETIME_FORMAT': "MMM dd, yyyy",
    }
