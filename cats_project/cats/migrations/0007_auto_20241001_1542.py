# Generated by Django 3.2.16 on 2024-10-01 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0006_auto_20241001_1525'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='score',
            name='unique_user_cat',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='user',
            new_name='owner',
        ),
        migrations.AddConstraint(
            model_name='score',
            constraint=models.UniqueConstraint(fields=('cat', 'owner'), name='unique_user_cat'),
        ),
    ]
