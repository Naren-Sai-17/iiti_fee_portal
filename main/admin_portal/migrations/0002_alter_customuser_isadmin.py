# Generated by Django 5.0.1 on 2024-03-12 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='isAdmin',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
