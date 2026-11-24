from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("employees", "0001_initial")]
    operations = [migrations.AddField(
        model_name="collectionrequest",
        name="payout_amount",
        field=models.DecimalField(decimal_places=2, default=150, max_digits=8),
    )]
