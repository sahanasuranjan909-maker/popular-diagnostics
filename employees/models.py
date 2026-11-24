from django.db import models
import uuid
from django.contrib.auth.models import User

class Employee(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = "available", "Available"
        BUSY = "busy", "Busy"
        OFFLINE = "offline", "Offline"
    employee_id = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="employee_profile")
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=6)
    email = models.EmailField(blank=True)
    availability = models.CharField(max_length=12, choices=Availability.choices, default=Availability.OFFLINE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    profile_picture = models.FileField(upload_to="employee_profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = "PD-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"

class CollectionRequest(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    case_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    collection_type = models.CharField(max_length=100)
    address = models.TextField()
    pin_code = models.CharField(max_length=6)
    payout_amount = models.DecimalField(max_digits=8, decimal_places=2, default=150)
    accepted_by = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_collections")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_number} - {self.customer_name}"
