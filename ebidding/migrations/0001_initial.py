# Generated by Django 3.1.6 on 2021-03-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('regid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=12)),
                ('mobile', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('role', models.CharField(max_length=10)),
                ('status', models.IntegerField()),
                ('info', models.CharField(max_length=100)),
            ],
        ),
    ]