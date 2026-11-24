from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0002_collectionrequest_payout_amount")]
    operations = [migrations.CreateModel(name="Employee", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("employee_id", models.CharField(max_length=30, unique=True)),
        ("full_name", models.CharField(max_length=120)),
        ("phone", models.CharField(max_length=20)),
        ("email", models.EmailField(blank=True, max_length=254)),
        ("availability", models.CharField(choices=[("available", "Available"), ("busy", "Busy"), ("offline", "Offline")], default="offline", max_length=12)),
        ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
    ])]
