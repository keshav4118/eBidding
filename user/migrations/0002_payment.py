# Generated by Django 3.1.6 on 2021-04-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('txnid', models.AutoField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField()),
                ('uid', models.CharField(max_length=70)),
                ('amount', models.IntegerField()),
                ('info', models.CharField(max_length=100)),
            ],
        ),
    ]