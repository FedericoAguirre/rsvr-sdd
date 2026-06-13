from django.db import migrations


def seed_clients(apps, schema_editor):
    Client = apps.get_model("clients", "Client")
    clients = [
        Client(first_name="Lucía", last_name="García", email="lucia@example.com", mobile="+5491110000001"),
        Client(first_name="Carlos", last_name="López", email="carlos@example.com", mobile="+5491110000002"),
        Client(first_name="María", last_name="Rodríguez", email="maria@example.com", mobile="+5491110000003"),
        Client(first_name="Pedro", last_name="Martínez", email="pedro@example.com", mobile="+5491110000004"),
        Client(first_name="Ana", last_name="Fernández", email="ana@example.com", mobile="+5491110000005"),
    ]
    Client.objects.bulk_create(clients)


def reverse_seed(apps, schema_editor):
    Client = apps.get_model("clients", "Client")
    Client.objects.filter(email__in=[
        "lucia@example.com",
        "carlos@example.com",
        "maria@example.com",
        "pedro@example.com",
        "ana@example.com",
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_clients, reverse_seed),
    ]
