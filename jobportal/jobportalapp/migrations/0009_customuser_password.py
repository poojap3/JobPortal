# Generated by Django 4.1.4 on 2023-03-26 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobportalapp", "0008_rename_password_customuser_user_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="password",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
