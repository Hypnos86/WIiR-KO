from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class PermissionChecker:
    def __init__(self, user, group_name, model_class=None):
        '''
        user: obiekt użytkownika
        group_name: nazwa grupy
        model_class: model Django
        '''
        self.user = user
        self.model_class = model_class
        self.group_name = group_name
        self.group = self._get_group()
        self.content_type = (
            ContentType.objects.get_for_model(model_class) if model_class else None)
        self.app_label = model_class._meta.app_label if model_class else None
        self.model_name = model_class._meta.model_name if model_class else None
        self.test = ContentType

    def _get_group(self):
        try:
            return Group.objects.get(name=self.group_name)
        except Group.DoesNotExist:
            return None

    def is_user_in_group(self) -> bool:
        """
        Sprawdza czy użytkownik nalezy do grupy o nazwie group_name
        """
        return self.user.groups.filter(name=self.group_name).exists()

    def has_permission(self, codename: str) -> bool:
        """
        Sprawdza czy grupa ma okreslone uprawnienie do danego modelu
        """
        if not self.group or not self.is_user_in_group() or not self.content_type:
            return False
        try:
            perm = Permission.objects.get(codename=codename, content_type=self.content_type)
        except Permission.DoesNotExist:
            return False

        return self.group.permissions.filter(id=perm.id).exists()

    def user_has_perm(self, codename: str) -> bool:
        """
        sprawda czy użytkownik ma pełne uprawnienie do app_label.codename,
        sprawdza uprawienia indywidualne, uprawnienie odziedziczone z grup
        SPRAWDZA UPRAWNIENIA UZYTKOWNIKA
        """
        if not self.model_class:
            return False
        full_codename = f"{self.app_label}.{codename}"
        return self.user.has_perm(full_codename)

    def can_view(self):
        """
        Sprawdza czy grupa ma uprawnienie
        """
        return self.has_permission(f'view_{self.model_name}')

    def can_add(self):
        """
        Sprawdza czy grupa ma uprawnienie
        """
        return self.has_permission(f'add_{self.model_name}')

    def can_change(self):
        """
        Sprawdza czy grupa ma uprawnienie
        """
        return self.has_permission(f'change_{self.model_name}')

    def can_delete(self):
        """
        Sprawdza czy grupa ma uprawnienie
        """
        return self.has_permission(f'delete_{self.model_class._meta.model_name}')
