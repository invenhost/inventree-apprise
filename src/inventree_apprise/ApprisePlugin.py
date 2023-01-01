"""Plugin to send notifications from InvenTree via Apprise."""

from plugin import InvenTreePlugin, registry
from plugin.mixins import SettingsMixin, BulkNotificationMethod
from django.utils.translation import gettext_lazy as _
import apprise


class PlgMixin:
    """Mixin to access plugin easier.

    This needs to be spit out to reference the class. Perks of python.
    """

    def get_plugin(self):
        """Return plugin reference."""
        return ApprisePlugin

class ApprisePlugin(SettingsMixin, InvenTreePlugin):
    """Send notifications from InvenTree via Apprise."""

    NAME = 'ApprisePlugin'
    SLUG = 'apprise'
    TITLE = "Apprise Notifications"
    SETTINGS = {
        'ENABLE_NOTIFICATION_APPRISE': {
            'name': _('Enable apprise notifications'),
            'description': _('Allow sending of event notifications via apprise'),
            'default': False,
            'validator': bool,
        },
        'NOTIFICATION_APPRISE_URL': {
            'name': _('Apprise URLs'),
            'description': _('URLs for notification enppoints, seperated by semicolons'),
            'protected': True,
        },
    }

    class SlackNotification(PlgMixin, BulkNotificationMethod):
        """Notificationmethod for delivery via Apprise."""

        METHOD_NAME = 'apprise'
        GLOBAL_SETTING = 'ENABLE_NOTIFICATION_APPRISE'

        def get_targets(self):
            """Not used by this method."""
            return self.targets

        def send_bulk(self):
            """Send the notifications out via slack."""

            instance = registry.plugins.get(self.get_plugin().NAME.lower())
            url = instance.get_setting('NOTIFICATION_APPRISE_URL')

            if not url:
                return False

            apobj = apprise.Apprise()

            # Add all of the notification services
            for notifiy_url in url.split(';'):
                apobj.add(notifiy_url)

            # Send notification out
            ret = apobj.notify(body=str(self.context['message']),title=str(self.context['name']))

            return bool(ret)
