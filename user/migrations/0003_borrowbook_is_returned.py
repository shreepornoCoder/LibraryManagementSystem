# Generated by Django 5.0.6 on 2024-08-10 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_borrowbook_borrowing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowbook',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
