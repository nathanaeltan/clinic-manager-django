# Generated by Django 3.2.25 on 2024-05-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20240510_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='procedures',
        ),
        migrations.AddField(
            model_name='appointment',
            name='procedures',
            field=models.ManyToManyField(to='core.Procedure'),
        ),
    ]
