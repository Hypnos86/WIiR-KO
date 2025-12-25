from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class PermissionChecker:
    @staticmethod
    def has_model_perm(user, model_class, actions=("view", "add", "change", "delete")) -> bool:
        # brak usera / niezalogowany
        if not user or not getattr(user, "is_authenticated", False):
            return False

        if user.is_superuser:
            return True

        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name

        return any(
            user.has_perm(f"{app_label}.{action}_{model_name}")
            for action in actions
        )
