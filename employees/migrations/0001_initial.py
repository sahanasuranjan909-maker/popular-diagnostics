from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="CollectionRequest", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("case_number", models.CharField(max_length=20, unique=True)),
        ("customer_name", models.CharField(max_length=100)),
        ("collection_type", models.CharField(max_length=100)),
        ("address", models.TextField()),
        ("pin_code", models.CharField(max_length=6)),
        ("status", models.CharField(choices=[("open", "Open"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="open", max_length=12)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
    ])]
