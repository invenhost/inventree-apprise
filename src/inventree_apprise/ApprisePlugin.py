"""Plugin to send notifications from InvenTree via Apprise."""

import logging

from django.contrib.auth.models import User
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

import apprise

from plugin import InvenTreePlugin, registry
from plugin.mixins import NotificationMixin, SettingsMixin

# Logger configuration
logger = logging.getLogger("inventree")


class ApprisePlugin(NotificationMixin, SettingsMixin, InvenTreePlugin):
    """Send notifications from InvenTree via Apprise."""

    NAME = "ApprisePlugin"
    SLUG = "apprise"
    TITLE = "Apprise Notifications"
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

        # Send notification out
        ret = apobj.notify(
            body=str(self.context["message"]), title=str(self.context["name"])
        )

        return bool(ret)
