# Generated by Django 5.0.1 on 2024-02-03 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0002_error_logs_mobileservices_logs_reports_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error_logs',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='mobileservices_logs',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='reports_logs',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='youtility_logs',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
        ),
    ]