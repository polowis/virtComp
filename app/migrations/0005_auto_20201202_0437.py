# Generated by Django 3.1.3 on 2020-12-02 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201129_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner_name',
            field=models.CharField(max_length=255),
        ),
    ]