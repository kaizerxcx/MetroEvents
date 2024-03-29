# Generated by Django 3.1.1 on 2021-11-16 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('middlename', models.CharField(default='NA', max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=3)),
                ('date_registered', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('receiver', models.CharField(max_length=500)),
                ('content', models.CharField(max_length=500)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('time', models.TimeField(auto_now=True)),
                ('date', models.DateField(auto_now=True)),
                ('isRead', models.BooleanField(default=False)),
                ('request_type', models.IntegerField(default=0)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to='user.user')),
            ],
            options={
                'db_table': 'Request',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('receiver', models.CharField(max_length=500)),
                ('content', models.CharField(max_length=500)),
                ('subject', models.CharField(max_length=100)),
                ('time', models.TimeField(auto_now=True)),
                ('date', models.DateField(auto_now=True)),
                ('isRead', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to='user.user')),
            ],
            options={
                'db_table': 'Notification',
            },
        ),
    ]
