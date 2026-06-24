from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from apps.payments.models import Payment


class Command(BaseCommand):
    help = _("Create default groups for payments module")

    def handle(self, *args, **options):
        operators, _ = Group.objects.get_or_create(name="Operators")
        admins, _ = Group.objects.get_or_create(name="Administrators")

        ct = ContentType.objects.get_for_model(Payment)
        perms = Permission.objects.filter(content_type=ct)
        operators.permissions.add(*perms)
        admins.permissions.add(*perms)

        self.stdout.write(
            self.style.SUCCESS(_("Groups created: Operators, Administrators")),
        )
