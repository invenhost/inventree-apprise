"""Plugin to send notifications from InvenTree via Apprise."""

import logging

from django.contrib.auth.models import User
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

import apprise

from plugin import InvenTreePlugin, registry
from plugin.mixins import NotificationMixin, SettingsMixin

from . import PLUGIN_VERSION

# Logger configuration
logger = logging.getLogger("inventree")


class ApprisePlugin(NotificationMixin, SettingsMixin, InvenTreePlugin):
    """Send notifications from InvenTree via Apprise."""

    NAME = "ApprisePlugin"
    SLUG = "apprise"
    TITLE = "Apprise Notifications"
    AUTHOR = "Matthias Mair"
    DESCRIPTION = "Send notifications from InvenTree via Apprise (over 130 services)"
    WEBSITE = "https://github.com/invenhost/inventree-apprise"
    VERSION = PLUGIN_VERSION

    SETTINGS = {
        "ENABLE_NOTIFICATION_APPRISE": {
            "name": _("Enable apprise notifications"),
            "description": _("Allow sending of event notifications via apprise"),
            "default": False,
            "validator": bool,
        },
        "NOTIFICATION_APPRISE_URL": {
            "name": _("Apprise URLs"),
            "description": _(
                "URLs for notification enppoints, separated by semicolons"
            ),
            "protected": True,
        },
    }

    def send_notification(
        self, target: Model, category: str, users: list[User], context: dict
    ) -> bool:
        """Send the notifications out via slack."""
        if not self.get_setting("ENABLE_NOTIFICATION_APPRISE"):
            logger.debug("Apprise notifications are disabled")
            return False

        url = self.get_setting("NOTIFICATION_APPRISE_URL")

        if not url:
            return False

        # Apprise specific stuff from here on out
        apobj = apprise.Apprise()

        # Add all of the notification services
        for notifiy_url in url.split(";"):
            apobj.add(notifiy_url)

        name = context.get("name")
        message = context.get("message")

        # Send notification out
        ret = apobj.notify(body=str(message), title=str(name))

        return bool(ret)
