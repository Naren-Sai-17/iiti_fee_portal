# Generated by Django 5.0.1 on 2024-03-29 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0003_alter_feeremission_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeremission',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='remission', serialize=False, to='admin_portal.students'),
        ),
    ]