# Generated by Django 4.1 on 2023-12-13 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_alter_customer_current_debt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='customer',
        ),
        migrations.AddField(
            model_name='loan',
            name='customer_id',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
