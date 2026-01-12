# your_parser_app/migrations/0003_auto_load_data.py
from django.db import migrations
from parser.management.commands.fill_database import Command

def load_initial_data(apps, schema_editor):
    # Импортируем и запускаем логику парсера
    cmd = Command()
    cmd.handle() # или ваша функция из tea_parser.py

class Migration(migrations.Migration):
    dependencies = [
        ('main_functionality', '0002_additive_basetaste_basetea_taste_and_more'), # предыдущая миграция
    ]
    operations = [
        migrations.RunPython(load_initial_data),
    ]