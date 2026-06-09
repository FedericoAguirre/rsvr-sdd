from django.core.management.base import BaseCommand
from apps.classes.models import ClassSlot
from apps.equipment.models import Equipment
from apps.clients.models import Client
from datetime import time


class Command(BaseCommand):
    help = "Seed initial data: class slots, equipment, and sample clients"

    def handle(self, *args, **options):
        self._create_class_slots()
        self._create_equipment()
        self._create_clients()
        self.stdout.write(self.style.SUCCESS("Data seeded successfully."))

    def _create_class_slots(self):
        if ClassSlot.objects.exists():
            self.stdout.write("  Class slots already exist, skipping.")
            return
        for day in range(5):
            for hour, minute in [(17, 30), (18, 30)]:
                ClassSlot.objects.create(
                    day_of_week=day, time=time(hour, minute), is_active=True
                )
        self.stdout.write(f"  Created {ClassSlot.objects.count()} class slots.")

    def _create_equipment(self):
        if Equipment.objects.exists():
            self.stdout.write("  Equipment already exists, skipping.")
            return
        items = [
            ("Treadmill 1", "treadmill"),
            ("Treadmill 2", "treadmill"),
            ("Stationary Bike 1", "bike"),
            ("Stationary Bike 2", "bike"),
            ("Elliptical 1", "elliptical"),
        ]
        for name, etype in items:
            Equipment.objects.create(name=name, equipment_type=etype)
        self.stdout.write(f"  Created {Equipment.objects.count()} equipment items.")

    def _create_clients(self):
        if Client.objects.exists():
            self.stdout.write("  Clients already exist, skipping.")
            return
        clients_data = [
            ("Alice", "Johnson", "alice@example.com", "+1-555-0101"),
            ("Bob", "Smith", "bob@example.com", "+1-555-0102"),
            ("Carol", "Davis", None, "+1-555-0103"),
            ("David", "Wilson", "david@example.com", None),
        ]
        for first, last, email, mobile in clients_data:
            Client.objects.create(
                first_name=first, last_name=last, email=email, mobile=mobile
            )
        self.stdout.write(f"  Created {Client.objects.count()} clients.")
