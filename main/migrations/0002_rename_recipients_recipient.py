# Generated by Django 5.0.2 on 2024-03-25 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="recipients",
            new_name="Recipient",
        ),
    ]
