# Generated by Django 5.2 on 2025-04-29 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxerstats', '0006_boxerstats_heart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boxerstats',
            old_name='stamina',
            new_name='endurance',
        ),
        migrations.AlterField(
            model_name='boxerstats',
            name='heart',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
