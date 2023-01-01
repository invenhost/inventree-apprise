"""Plugin to send notifications from InvenTree via Apprise."""

from plugin import InvenTreePlugin


class ApprisePlugin(InvenTreePlugin):
    """Send notifications from InvenTree via Apprise."""

    NAME = 'ApprisePlugin'
    SLUG = 'apprise'
    TITLE = "Apprise Notifications"
