"""
Default implementation when not overriden
"""

from __future__ import unicode_literals

from django.core import validators
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..compat import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    # Only way I found out to remove the ``UniqueValidator``. We are not
    # interested to create new instances here.
    slug = serializers.CharField(source='username', validators=[
        validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'),
            'invalid')],
        help_text=_("Effectively the username. The variable is named `slug`"\
            " such that front-end code can be re-used between Organization"\
            " and User records."))
    email = serializers.EmailField(read_only=True,
        help_text=_("E-mail address for the user"))
    created_at = serializers.DateTimeField(source='date_joined', required=False,
        help_text=_("Date/time of creation (in ISO format)"))
    last_login = serializers.DateTimeField(required=False,
        help_text=_("Date/time of last login (in ISO format)"))
    full_name = serializers.SerializerMethodField(
        help_text=_("Full name for the contact (effectively first name"\
        " followed by last name)"))

    class Meta:
        model = get_user_model()
        fields = ('slug', 'email', 'full_name', 'created_at', 'last_login')
        read_only = ('full_name', 'created_at', 'last_login')

    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()
