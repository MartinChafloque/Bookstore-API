# Generated by Django 3.2.3 on 2023-12-10 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='imagen',
            field=models.TextField(null=True),
        ),
    ]
