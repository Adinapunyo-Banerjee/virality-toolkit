# Generated by Django 4.2 on 2023-05-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tokenBalance",
            field=models.IntegerField(default=100),
        ),
    ]
