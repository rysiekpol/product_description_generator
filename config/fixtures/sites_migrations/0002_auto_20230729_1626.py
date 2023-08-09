from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def insert_sites(apps, schema_editor):
    """Populate the sites model"""
    Site = apps.get_model("sites", "Site")

    # Register SITE_ID = 1
    Site.objects.update_or_create(
        pk=settings.SITE_ID, defaults={"domain": "masze.pl", "name": "api.masze.pl"}
    )


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [migrations.RunPython(insert_sites)]
