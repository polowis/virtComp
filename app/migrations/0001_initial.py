# Generated by Django 3.1.3 on 2020-12-16 07:46

import app.core.util.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('buy_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('rent_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('cost_growth', models.DecimalField(decimal_places=3, max_digits=5)),
                ('upgrade_growth', models.DecimalField(decimal_places=3, max_digits=5)),
                ('base_employees', models.IntegerField()),
                ('employees_growth', models.DecimalField(decimal_places=3, max_digits=5)),
                ('base_storage', models.IntegerField()),
                ('storage_growth', models.DecimalField(decimal_places=3, max_digits=5)),
                ('can_sell', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CommunityBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=4, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('continent', models.CharField(default='asia', max_length=255)),
                ('balance', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('popularity', models.IntegerField(default=0)),
                ('reputation', models.IntegerField(default=0)),
                ('qualification', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('rent', models.DecimalField(decimal_places=4, max_digits=20)),
                ('max_land_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('min_land_cost', models.DecimalField(decimal_places=4, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Landscape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('level', models.IntegerField()),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('continent', models.CharField(max_length=255)),
                ('buy_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('rent_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('continent_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('continent_rent', models.DecimalField(decimal_places=4, max_digits=20)),
                ('is_buy', models.BooleanField(default=False)),
                ('is_rent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('last_collected_money_at', models.DateTimeField(null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='OwnerBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=4, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('time_to_produce', models.IntegerField()),
                ('cost_attempt', models.DecimalField(decimal_places=4, max_digits=20)),
                ('probability_per_attempt', models.FloatField()),
                ('factory_type', models.CharField(max_length=255)),
                ('continent', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
                ('electric_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('water_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('gas_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('quantity_upon_produced', models.IntegerField()),
                ('unlock_at_building_level', models.IntegerField()),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.buildingtype')),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('building_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('building_type', models.CharField(max_length=255)),
                ('building_name', models.CharField(max_length=255)),
                ('current_level', models.IntegerField()),
                ('company_name', models.CharField(max_length=255)),
                ('current_storage', models.IntegerField()),
                ('max_storage', models.IntegerField()),
                ('current_employee', models.IntegerField(default=0)),
                ('max_employee', models.IntegerField()),
                ('is_buy', models.BooleanField(default=False)),
                ('is_rent', models.BooleanField(default=False)),
                ('rent_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('buy_cost', models.DecimalField(decimal_places=4, max_digits=20)),
                ('landscape', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.landscape')),
                ('last_collected_money_at', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
        ),
    ]
