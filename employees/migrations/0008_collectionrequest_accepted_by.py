from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("employees", "0007_employee_verification_flags")]
    operations = [migrations.AddField(model_name="collectionrequest", name="accepted_by", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="accepted_collections", to="employees.employee"))]
