# Generated by Django 2.2.1 on 2019-05-09 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190509_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zip',
            name='Zip',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
