from django.db import migrations


def seed_climber_equipments(apps, schema_editor):
    Equipment = apps.get_model("equipment", "Equipment")
    equipments = [
        Equipment(name=f"E{i:02d}", equipment_type="climber")
        for i in range(1, 31)
    ]
    Equipment.objects.bulk_create(equipments)


def reverse_seed(apps, schema_editor):
    Equipment = apps.get_model("equipment", "Equipment")
    Equipment.objects.filter(equipment_type="climber", name__startswith="E").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("equipment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_climber_equipments, reverse_seed),
    ]
