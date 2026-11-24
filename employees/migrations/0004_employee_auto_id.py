from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0003_employee")]
    operations = [migrations.AlterField(model_name="employee", name="employee_id", field=models.CharField(blank=True, editable=False, max_length=30, unique=True))]
