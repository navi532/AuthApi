# Generated by Django 3.2.8 on 2022-02-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapi', '0004_alter_loginhistory_is_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginhistory',
            name='is_success',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
