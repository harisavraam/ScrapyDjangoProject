# Generated by Django 3.2.6 on 2021-12-12 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_competitoranalysismodel_retry_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CityId', models.CharField(max_length=50)),
                ('cid', models.CharField(max_length=50)),
                ('weather_state_name', models.CharField(max_length=50)),
                ('weather_state_abbr', models.CharField(max_length=50)),
                ('wind_direction_compass', models.CharField(max_length=50)),
                ('created', models.DateTimeField()),
                ('applicable_date', models.DateField()),
                ('min_temp', models.DecimalField(decimal_places=14, max_digits=24)),
                ('max_temp', models.DecimalField(decimal_places=14, max_digits=24)),
                ('the_temp', models.DecimalField(decimal_places=14, max_digits=24)),
                ('wind_speed', models.DecimalField(decimal_places=14, max_digits=24)),
                ('wind_direction', models.DecimalField(decimal_places=14, max_digits=24)),
                ('air_pressure', models.DecimalField(decimal_places=14, max_digits=24)),
                ('humidity', models.IntegerField()),
                ('visibility', models.DecimalField(decimal_places=14, max_digits=24)),
                ('predictability', models.IntegerField()),
            ],
        ),
    ]