# Generated by Django 3.2.25 on 2024-05-09 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')], max_length=150, null=True),
        ),
    ]
