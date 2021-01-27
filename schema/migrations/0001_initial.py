# Generated by Django 3.1.5 on 2021-01-27 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('column_separator', models.CharField(choices=[(',', 'Comma'), (';', 'Semicolon'), ('\t', 'Tab'), ('|', 'Pipe')], max_length=1)),
                ('string_character', models.CharField(choices=[('"', 'Double quote'), ("'", 'Single quote')], max_length=1)),
                ('schema_columns', models.JSONField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
