# Generated by Django 4.1.6 on 2023-02-23 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0003_alter_store_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partyticket',
            name='venue',
        ),
    ]
