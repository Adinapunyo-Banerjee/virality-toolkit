# Generated by Django 4.0.7 on 2023-05-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_ispromotable_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isPromotable',
            field=models.BooleanField(default=True),
        ),
    ]
