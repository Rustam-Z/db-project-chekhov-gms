# Generated by Django 3.0 on 2022-04-24 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('transaction_number', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Transaction number')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Amount')),
                ('card_type', models.CharField(choices=[('V', 'Visa'), ('M', 'Mastercard'), ('U', 'Uzcard')], max_length=1, verbose_name='Card type')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('ssn', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='SSN')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(default=0, verbose_name='Age')),
                ('gender', models.CharField(choices=[(None, 'Choose gender'), ('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'All people',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Registration number')),
                ('timestamp', models.TimeField(verbose_name='Registration time')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, verbose_name='Subscription number')),
                ('type', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, verbose_name='Subscription type')),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gym.Person')),
                ('licence_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Licence number')),
                ('salary', models.IntegerField(default=0, null=True, verbose_name='Salary per year in $')),
                ('specialization', models.CharField(max_length=255, null=True, verbose_name='Specialization')),
            ],
            options={
                'verbose_name': 'Coach',
                'verbose_name_plural': 'Coaches',
            },
            bases=('gym.person',),
        ),
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], unique=True)),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
            ],
            options={
                'verbose_name': 'Working hours',
                'verbose_name_plural': 'Working hours',
                'ordering': ('weekday', 'from_hour'),
                'unique_together': {('weekday', 'from_hour', 'to_hour')},
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('work_hours', models.ManyToManyField(to='gym.WorkingHours', verbose_name='Working hours')),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Gym name')),
                ('capacity', models.IntegerField(default=0, verbose_name='Gym capacity')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gym.Location')),
                ('coaches', models.ManyToManyField(to='gym.Coach', verbose_name='Coaches')),
            ],
            options={
                'verbose_name': 'Gym',
                'verbose_name_plural': 'Gyms',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('serial_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Gym')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gym.Person')),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Employee ID')),
                ('salary', models.IntegerField(default=0, verbose_name='Salary per year in $')),
                ('seniority_level', models.CharField(choices=[(None, 'Choose seniority level'), ('L1', 'Junior'), ('L2', 'Middle'), ('L3', 'Senior'), ('L4', 'Lead')], max_length=2, verbose_name='Seniority Level')),
                ('working_hours', models.ManyToManyField(to='gym.WorkingHours', verbose_name='Working hours')),
            ],
            bases=('gym.person',),
        ),
        migrations.AddField(
            model_name='gym',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.Manager'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gym.Person')),
                ('account_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Account number')),
                ('payment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Payment')),
                ('registration', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gym.Registration')),
                ('subscription', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Subscription')),
            ],
            bases=('gym.person',),
        ),
    ]
