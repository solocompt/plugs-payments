"""
Plugs Payments Settings
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


MANDATORY_SETTINGS = ['ANTI_PHISHING_KEY', 'ENTITY', 'SUBENTITY']
PROJECT_SETTINGS = getattr(settings, 'PLUGS_PAYMENTS', {})

for setting in MANDATORY_SETTINGS:
    try:
        PROJECT_SETTINGS[setting]
    except KeyError:
        raise ImproperlyConfigured('Missing setting: PLUGS_PAYMENTS[\'{0}\']'.format(setting))

plugs_payments_settings = PROJECT_SETTINGS
