# Generated by Django 3.0.6 on 2022-11-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name Printer')),
                ('api_key', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Key access API')),
                ('check_type', models.CharField(blank=True, choices=[('kitchen', 'kitchen'), ('client', 'client')], max_length=10, null=True, verbose_name='Check type')),
                ('point_id', models.IntegerField(verbose_name='Point printer')),
            ],
            options={
                'verbose_name': 'Printer',
                'verbose_name_plural': 'Printers',
            },
        ),
    ]