# Generated by Django 4.2.7 on 2024-03-02 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_edu", "0006_alter_subscription_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="цена"
            ),
        ),
    ]
