# Generated by Django 4.1.6 on 2023-02-16 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0002_store_partyticket_provider'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'verbose_name': 'Provider'},
        ),
    ]
