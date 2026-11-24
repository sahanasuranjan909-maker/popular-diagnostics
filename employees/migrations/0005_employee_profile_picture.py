from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0004_employee_auto_id")]
    operations = [migrations.AddField(model_name="employee", name="profile_picture", field=models.FileField(blank=True, null=True, upload_to="employee_profiles/"))]
