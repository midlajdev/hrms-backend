from apps.users.models import AdminActionLog

def log_admin_action(admin, action, target_type, target_id):
    AdminActionLog.objects.create(
        admin=admin,
        action=action,
        target_type=target_type,
        target_id=target_id,
    )