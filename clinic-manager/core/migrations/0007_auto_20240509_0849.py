# Generated by Django 3.2.25 on 2024-05-09 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_patient_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='patient',
            name='id_number',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.CreateModel(
            name='PatientMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.CharField(max_length=100)),
                ('frequency', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.patient')),
            ],
        ),
        migrations.AddField(
            model_name='medication',
            name='patients',
            field=models.ManyToManyField(related_name='medications', through='core.PatientMedication', to='core.Patient'),
        ),
    ]
