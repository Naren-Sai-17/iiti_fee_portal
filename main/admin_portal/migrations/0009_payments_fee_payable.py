# Generated by Django 5.0.1 on 2024-04-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0008_rename_base_tution_fee_students_base_tuition_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='fee_payable',
            field=models.IntegerField(default=0),
        ),
    ]