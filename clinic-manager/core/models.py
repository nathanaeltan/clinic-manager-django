from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have valid email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=150,
        null=True,
        choices=[
            ("doctor", "Doctor"),
            ("nurse", "Nurse"),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=150, unique=True)
    gender = models.CharField(
        max_length=100,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
        ],
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Medication(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    patients = models.ManyToManyField(
        "Patient", through="PatientMedication", related_name="medications"
    )

    def __str__(self):
        return self.name


class PatientMedication(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    medication = models.ForeignKey("Medication", on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.medication}"

class Procedure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    procedures = models.ManyToManyField(Procedure)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient','start_time'], name='unique_appointment_time_per_patient')
        ]

    def clean(self):
        # Check if the appointment end time is after the start time
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

        # Check if there's any overlapping appointment for the same doctor
        overlapping_appointments = Appointment.objects.filter(
            patient=self.patient,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if self.pk:
            overlapping_appointments = overlapping_appointments.exclude(pk=self.pk)  # Exclude self if updating
        if overlapping_appointments.exists():
            raise ValidationError("Appointment timing overlaps with existing appointment")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the model
        super().save(*args, **kwargs)
