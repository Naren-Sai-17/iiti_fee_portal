# Generated by Django 4.2.6 on 2024-03-23 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0005_feestructure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='mess_rebate',
            field=models.IntegerField(default=0),
        ),
    ]
