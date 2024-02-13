# Generated by Django 5.0.1 on 2024-02-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('log_level', models.CharField(max_length=20)),
                ('method_name', models.CharField(max_length=255)),
                ('log_message', models.TextField()),
                ('traceback', models.TextField()),
            ],
            options={
                'db_table': 'error_logs',
            },
        ),
        migrations.CreateModel(
            name='Mobileservices_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('log_level', models.CharField(max_length=20)),
                ('method_name', models.CharField(max_length=255)),
                ('log_message', models.TextField()),
            ],
            options={
                'db_table': 'mobileservices_logs',
            },
        ),
        migrations.CreateModel(
            name='Reports_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('log_level', models.CharField(max_length=20)),
                ('method_name', models.CharField(max_length=255)),
                ('log_message', models.TextField()),
            ],
            options={
                'db_table': 'reports_logs',
            },
        ),
    ]
