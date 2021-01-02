# Generated by Django 3.1.3 on 2021-01-02 07:14

import app.core.util.base
import app.models.core.agent.agent_stats
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('continent', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
        ),
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
                ('can_produce', models.BooleanField()),
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
                ('is_selling', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
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
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('continent', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.DecimalField(decimal_places=4, max_digits=20)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgentStats',
            fields=[
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='agent', serialize=False, to='app.agentcustomer')),
                ('qualification', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('productivity', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('communication', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('creativity', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('leadership', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('learning', models.IntegerField(default=app.models.core.agent.agent_stats.random_score)),
                ('stress', models.IntegerField(default=0)),
                ('emotion', models.IntegerField(default=100)),
                ('salary', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('hour_of_work_per_day', models.IntegerField(default=0)),
                ('is_rest', models.BooleanField(default=True)),
                ('is_employed', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField()),
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
                ('current_storage', models.IntegerField(default=0)),
                ('max_storage', models.IntegerField()),
                ('current_employees', models.IntegerField(default=0)),
                ('max_employees', models.IntegerField()),
                ('is_buy', models.BooleanField(default=False)),
                ('is_rent', models.BooleanField(default=False)),
                ('rent_cost', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('buy_cost', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('landscape', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.landscape')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('last_collected_money_at', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.IntegerField()),
                ('sender_id', models.CharField(max_length=255)),
                ('receiver_id', models.CharField(max_length=255)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='app.company')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.company')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('money', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='app.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('quantity', models.IntegerField()),
                ('discount', models.DecimalField(decimal_places=4, max_digits=20)),
                ('name', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('bought_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
                ('item_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='AgentStatsTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.IntegerField()),
                ('productivity', models.IntegerField()),
                ('communication', models.IntegerField()),
                ('creativity', models.IntegerField()),
                ('leadership', models.IntegerField()),
                ('learning', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.agentcustomer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStored',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(default=app.core.util.base.generate_unique_id, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.building')),
            ],
        ),
    ]
