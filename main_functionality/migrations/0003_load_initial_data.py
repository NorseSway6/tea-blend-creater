from django.db import migrations
from parser.management.commands.fill_database import Command

def load_initial_data(apps, schema_editor):
    cmd = Command()
    cmd.handle()

class Migration(migrations.Migration):
    dependencies = [
        ('main_functionality', '0002_additive_basetaste_basetea_taste_and_more'),
    ]
    operations = [
        migrations.RunPython(load_initial_data),
    ]