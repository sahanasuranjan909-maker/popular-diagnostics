from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("auth", "0012_alter_user_first_name_max_length"), ("employees", "0005_employee_profile_picture")]
    operations = [migrations.AddField(model_name="employee", name="user", field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="employee_profile", to="auth.user"))]
