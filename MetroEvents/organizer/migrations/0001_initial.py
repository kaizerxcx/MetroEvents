# Generated by Django 3.1.1 on 2021-11-16 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='user.user')),
                ('org_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_accepted', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'Organizer',
            },
            bases=('user.user',),
        ),
    ]
