# Generated by Django 5.0.1 on 2024-03-28 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0002_feeremission_alter_students_fee_arrear_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeremission',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='admin_portal.students'),
        ),
    ]