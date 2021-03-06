from .models import Notification
import logging

logger = logging.getLogger(__name__)

def notify(user, title, message=None, level='info'):
    notif = Notification()
    notif.user = user
    notif.title = title
    if not message:
        message = title
    notif.message = message
    notif.level = level
    notif.save()
    logger.info("Created notification %s" % notif)
