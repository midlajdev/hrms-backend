import logging

from apps.ai.models import AuditLog

logger = logging.getLogger(__name__)


class LoggingService:

    @staticmethod
    def log_action(user, action, description):

        logger.info(description)

        AuditLog.objects.create(
            user=user,
            action=action,
            description=description
        )

    @staticmethod
    def log_error(error):

        logger.exception(error)