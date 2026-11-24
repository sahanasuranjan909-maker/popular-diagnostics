from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0008_collectionrequest_accepted_by")]
    operations = [migrations.AddField(model_name="employee", name="pin_code", field=models.CharField(default="000000", max_length=6))]
