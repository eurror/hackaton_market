# Generated by Django 4.1.5 on 2023-01-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254,
                 primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
