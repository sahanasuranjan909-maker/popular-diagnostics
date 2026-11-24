from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0006_employee_user")]
    operations = [migrations.AddField(model_name="employee", name="email_verified", field=models.BooleanField(default=False)), migrations.AddField(model_name="employee", name="phone_verified", field=models.BooleanField(default=False))]
